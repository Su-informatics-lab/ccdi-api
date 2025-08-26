"""
Subject router for CCDI API.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import Optional, List
import logging

from app.models import (
    Subject, SubjectsResponse, Summary, EntitySummary, CountResults, CountResult,
    SubjectIdentifier, NamespaceIdentifier, MetadataField, SubjectMetadata,
    ErrorResponse, Error, FieldDescriptions, FieldDescription
)
from app.services.data_loader import DataLoader

logger = logging.getLogger(__name__)
router = APIRouter()


def get_data_loader(request: Request) -> DataLoader:
    """Dependency to get the data loader from app state."""
    return request.app.state.data_loader


def create_subject_from_row(row: dict) -> Subject:
    """Create a Subject model from a DataFrame row."""
    # Create namespace identifier
    namespace = NamespaceIdentifier(
        organization=row.get('namespace_organization', ''),
        name=row.get('namespace_name', '')
    )
    
    # Create subject identifier
    subject_id = SubjectIdentifier(
        namespace=namespace,
        name=row.get('subject_name', '')
    )
    
    # Create metadata fields
    metadata = SubjectMetadata()
    
    if row.get('sex'):
        metadata.sex = MetadataField(value=row['sex'])
    
    if row.get('race'):
        metadata.race = [MetadataField(value=row['race'])]
    
    if row.get('ethnicity'):
        metadata.ethnicity = MetadataField(value=row['ethnicity'])
    
    if row.get('identifiers'):
        metadata.identifiers = [MetadataField(value=row['identifiers'])]
    
    if row.get('vital_status'):
        metadata.vital_status = MetadataField(value=row['vital_status'])
    
    if row.get('age_at_vital_status'):
        metadata.age_at_vital_status = MetadataField(value=row['age_at_vital_status'])
    
    # Handle both possible column names for associated diagnoses
    diagnosis_field = row.get('associated_diagnoses') or row.get('associated_diagnosis')
    if diagnosis_field:
        metadata.associated_diagnoses = [MetadataField(value=diagnosis_field)]
    
    return Subject(
        id=subject_id,
        kind=row.get('kind', 'Participant'),
        metadata=metadata
    )


@router.get("", response_model=SubjectsResponse)
async def get_subjects(
    data_loader: DataLoader = Depends(get_data_loader),
    sex: Optional[str] = Query(None, description="Filter by sex"),
    race: Optional[str] = Query(None, description="Filter by race"),
    ethnicity: Optional[str] = Query(None, description="Filter by ethnicity"),
    identifiers: Optional[str] = Query(None, description="Filter by identifiers"),
    vital_status: Optional[str] = Query(None, description="Filter by vital status"),
    age_at_vital_status: Optional[str] = Query(None, description="Filter by age at vital status"),
    depositions: Optional[str] = Query(None, description="Filter by depositions"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, description="Number of results per page")
):
    """Get subjects with optional filtering and pagination."""
    try:
        df = data_loader.subjects_df
        if df.empty:
            return SubjectsResponse(
                summary=EntitySummary(total=0),
                data=[]
            )
        
        # Apply filters
        filters = {
            'sex': sex,
            'race': race,
            'ethnicity': ethnicity,
            'identifiers': identifiers,
            'vital_status': vital_status,
            'age_at_vital_status': age_at_vital_status
        }
        
        filtered_df = data_loader.filter_dataframe(df, filters)
        total_count = len(filtered_df)
        
        # Apply pagination
        paginated_df = data_loader.paginate_dataframe(filtered_df, page, per_page)
        
        # Convert to Subject models
        subjects = []
        for _, row in paginated_df.iterrows():
            try:
                subject = create_subject_from_row(row.to_dict())
                subjects.append(subject)
            except Exception as e:
                logger.warning(f"Failed to create subject from row: {e}")
        
        return SubjectsResponse(
            summary=EntitySummary(total=total_count),
            data=subjects
        )
        
    except Exception as e:
        logger.error(f"Error getting subjects: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{organization}/{namespace}/{name}", response_model=Subject)
async def get_subject(
    organization: str,
    namespace: str,
    name: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get a specific subject by identifier."""
    try:
        row = data_loader.get_subject_by_id(organization, namespace, name)
        if not row:
            raise HTTPException(
                status_code=404,
                detail={
                    "errors": [{
                        "kind": "NotFound",
                        "entity": f"Subject with namespace '{organization}/{namespace}' and name '{name}'",
                        "message": f"Subject with namespace '{organization}/{namespace}' and name '{name}' not found."
                    }]
                }
            )
        
        return create_subject_from_row(row)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting subject {organization}/{namespace}/{name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/by/{field}/count", response_model=CountResults)
async def get_subjects_count_by_field(
    field: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Group subjects by the specified field and return counts."""
    try:
        df = data_loader.subjects_df
        if df.empty:
            return CountResults(
                summary=EntitySummary(total=0),
                data=[]
            )
        
        # Check if field is supported
        supported_fields = ['sex', 'race', 'ethnicity', 'identifiers', 'vital_status', 'kind']
        if field not in supported_fields:
            raise HTTPException(
                status_code=422,
                detail={
                    "errors": [{
                        "kind": "UnsupportedField",
                        "field": field,
                        "reason": "This field is not present for subjects.",
                        "message": f"Field '{field}' is not supported: this field is not present for subjects."
                    }]
                }
            )
        
        counts = data_loader.count_by_field(df, field)
        total = sum(item['count'] for item in counts)
        
        count_results = [CountResult(name=item['name'], count=item['count']) for item in counts]
        
        return CountResults(
            summary=EntitySummary(total=total),
            data=count_results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting subject counts by {field}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/summary", response_model=Summary)
async def get_subjects_summary(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get summary information for subjects."""
    try:
        subject_count = len(data_loader.subjects_df) if not data_loader.subjects_df.empty else 0
        sample_count = len(data_loader.samples_df) if not data_loader.samples_df.empty else 0
        file_count = len(data_loader.files_df) if not data_loader.files_df.empty else 0
        
        return Summary(
            subjects=EntitySummary(total=subject_count),
            samples=EntitySummary(total=sample_count),
            files=EntitySummary(total=file_count)
        )
        
    except Exception as e:
        logger.error(f"Error getting subjects summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Experimental endpoint for diagnosis search
@router.get("-diagnosis", response_model=SubjectsResponse)
async def get_subjects_by_diagnosis(
    data_loader: DataLoader = Depends(get_data_loader),
    search: Optional[str] = Query(None, description="Search term for diagnosis"),
    sex: Optional[str] = Query(None, description="Filter by sex"),
    race: Optional[str] = Query(None, description="Filter by race"),
    ethnicity: Optional[str] = Query(None, description="Filter by ethnicity"),
    identifiers: Optional[str] = Query(None, description="Filter by identifiers"),
    vital_status: Optional[str] = Query(None, description="Filter by vital status"),
    age_at_vital_status: Optional[str] = Query(None, description="Filter by age at vital status"),
    depositions: Optional[str] = Query(None, description="Filter by depositions"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, description="Number of results per page")
):
    """Experimental: Filter subjects by free-text diagnosis search."""
    try:
        df = data_loader.subjects_df
        if df.empty:
            return SubjectsResponse(
                summary=EntitySummary(total=0),
                data=[]
            )
        
        # Apply diagnosis search filter (case-insensitive contains)
        if search:
            # Check both possible column names for diagnosis
            if 'associated_diagnoses' in df.columns:
                diagnosis_mask = df['associated_diagnoses'].str.contains(search, case=False, na=False)
            elif 'associated_diagnosis' in df.columns:
                diagnosis_mask = df['associated_diagnosis'].str.contains(search, case=False, na=False)
            else:
                diagnosis_mask = df.index == df.index  # No filtering if column doesn't exist
            df = df[diagnosis_mask]
        
        # Apply other filters
        filters = {
            'sex': sex,
            'race': race,
            'ethnicity': ethnicity,
            'identifiers': identifiers,
            'vital_status': vital_status,
            'age_at_vital_status': age_at_vital_status
        }
        
        filtered_df = data_loader.filter_dataframe(df, filters)
        total_count = len(filtered_df)
        
        # Apply pagination
        paginated_df = data_loader.paginate_dataframe(filtered_df, page, per_page)
        
        # Convert to Subject models
        subjects = []
        for _, row in paginated_df.iterrows():
            try:
                subject = create_subject_from_row(row.to_dict())
                subjects.append(subject)
            except Exception as e:
                logger.warning(f"Failed to create subject from row: {e}")
        
        return SubjectsResponse(
            summary=EntitySummary(total=total_count),
            data=subjects
        )
        
    except Exception as e:
        logger.error(f"Error getting subjects by diagnosis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
