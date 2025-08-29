"""
Sample router for CCDI API.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import Optional
import logging

from app.models import (
    Sample, SamplesResponse, EntitySummary, EntityCounts, CountResults, CountResult, EntityPureCounts, EntityPureSummary,
    SampleIdentifier, SubjectIdentifier, NamespaceIdentifier, MetadataField, SampleMetadata,
    PageInfo
)
from app.services.data_loader import DataLoader

logger = logging.getLogger(__name__)
router = APIRouter()


def get_data_loader(request: Request) -> DataLoader:
    """Dependency to get the data loader from app state."""
    return request.app.state.data_loader


def create_sample_from_row(row: dict) -> Sample:
    """Create a Sample model from a DataFrame row."""
    # Create namespace identifier
    namespace = NamespaceIdentifier(
        organization=row.get('namespace_organization', ''),
        name=row.get('namespace_name', '')
    )
    
    # Create sample identifier
    sample_id = SampleIdentifier(
        namespace=namespace,
        name=row.get('sample_name', '')
    )
    
    # Create subject namespace identifier
    subject_namespace = NamespaceIdentifier(
        organization=row.get('subject_namespace_organization', ''),
        name=row.get('subject_namespace_name', '')
    )
    
    # Create subject identifier
    subject_id = SubjectIdentifier(
        namespace=subject_namespace,
        name=row.get('subject_name', '')
    )
    
    # Create metadata fields
    metadata = SampleMetadata()
    
    if row.get('disease_phase'):
        metadata.disease_phase = MetadataField(value=row['disease_phase'])
    
    if row.get('anatomical_sites'):
        metadata.anatomical_sites = [MetadataField(value=row['anatomical_sites'])]
    
    if row.get('library_selection_method'):
        metadata.library_selection_method = MetadataField(value=row['library_selection_method'])
    
    if row.get('library_strategy'):
        metadata.library_strategy = MetadataField(value=row['library_strategy'])
    
    if row.get('library_source_material'):
        metadata.library_source_material = MetadataField(value=row['library_source_material'])
    
    if row.get('preservation_method'):
        metadata.preservation_method = MetadataField(value=row['preservation_method'])
    
    if row.get('tumor_grade'):
        metadata.tumor_grade = MetadataField(value=row['tumor_grade'])
    
    if row.get('specimen_molecular_analyte_type'):
        metadata.specimen_molecular_analyte_type = MetadataField(value=row['specimen_molecular_analyte_type'])
    
    if row.get('tissue_type'):
        metadata.tissue_type = MetadataField(value=row['tissue_type'])
    
    if row.get('tumor_classification'):
        metadata.tumor_classification = MetadataField(value=row['tumor_classification'])
    
    if row.get('age_at_diagnosis'):
        metadata.age_at_diagnosis = MetadataField(value=row['age_at_diagnosis'])
    
    if row.get('age_at_collection'):
        metadata.age_at_collection = MetadataField(value=row['age_at_collection'])
    
    if row.get('tumor_tissue_morphology'):
        metadata.tumor_tissue_morphology = MetadataField(value=row['tumor_tissue_morphology'])
    
    if row.get('diagnosis'):
        metadata.diagnosis = MetadataField(value=row['diagnosis'])
    
    return Sample(
        id=sample_id,
        subject=subject_id,
        metadata=metadata
    )


@router.get("", response_model=SamplesResponse)
async def get_samples(
    data_loader: DataLoader = Depends(get_data_loader),
    disease_phase: Optional[str] = Query(None, description="Filter by disease phase"),
    anatomical_sites: Optional[str] = Query(None, description="Filter by anatomical sites"),
    library_selection_method: Optional[str] = Query(None, description="Filter by library selection method"),
    library_strategy: Optional[str] = Query(None, description="Filter by library strategy"),
    library_source_material: Optional[str] = Query(None, description="Filter by library source material"),
    preservation_method: Optional[str] = Query(None, description="Filter by preservation method"),
    tumor_grade: Optional[str] = Query(None, description="Filter by tumor grade"),
    specimen_molecular_analyte_type: Optional[str] = Query(None, description="Filter by specimen molecular analyte type"),
    tissue_type: Optional[str] = Query(None, description="Filter by tissue type"),
    tumor_classification: Optional[str] = Query(None, description="Filter by tumor classification"),
    age_at_diagnosis: Optional[str] = Query(None, description="Filter by age at diagnosis"),
    age_at_collection: Optional[str] = Query(None, description="Filter by age at collection"),
    tumor_tissue_morphology: Optional[str] = Query(None, description="Filter by tumor tissue morphology"),
    depositions: Optional[str] = Query(None, description="Filter by depositions"),
    diagnosis: Optional[str] = Query(None, description="Filter by diagnosis"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, description="Number of results per page")
):
    """Get samples with optional filtering and pagination."""
    try:
        df = data_loader.samples_df
        if df.empty:
            page_info = PageInfo(
                page=page,
                per_page=per_page,
                total_pages=0,
                total_count=0
            )
            return SamplesResponse(
                summary=EntitySummary(counts=EntityCounts(all=0, current=0)),
                page_info=page_info,
                data=[]
            )
        
        # Apply filters
        filters = {
            'disease_phase': disease_phase,
            'anatomical_sites': anatomical_sites,
            'library_selection_method': library_selection_method,
            'library_strategy': library_strategy,
            'library_source_material': library_source_material,
            'preservation_method': preservation_method,
            'tumor_grade': tumor_grade,
            'specimen_molecular_analyte_type': specimen_molecular_analyte_type,
            'tissue_type': tissue_type,
            'tumor_classification': tumor_classification,
            'age_at_diagnosis': age_at_diagnosis,
            'age_at_collection': age_at_collection,
            'tumor_tissue_morphology': tumor_tissue_morphology,
            'diagnosis': diagnosis
        }
        
        filtered_df = data_loader.filter_dataframe(df, filters)
        total_count = len(filtered_df)
        # Calculate pagination
        total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 0
        page_info = PageInfo(
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            total_count=total_count
        )
        
        # Apply pagination
        paginated_df = data_loader.paginate_dataframe(filtered_df, page, per_page)
        
        # Convert to Sample models
        samples = []
        for _, row in paginated_df.iterrows():
            try:
                sample = create_sample_from_row(row.to_dict())
                samples.append(sample)
            except Exception as e:
                logger.warning(f"Failed to create sample from row: {e}")
        
        return SamplesResponse(
            summary=EntitySummary(counts=EntityCounts(all=total_count, current=len(samples))),
            page_info=page_info,
            data=samples
        )
        
    except Exception as e:
        logger.error(f"Error getting samples: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{organization}/{namespace}/{name}", response_model=Sample)
async def get_sample(
    organization: str,
    namespace: str,
    name: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get a specific sample by identifier."""
    try:
        row = data_loader.get_sample_by_id(organization, namespace, name)
        if not row:
            raise HTTPException(
                status_code=404,
                detail={
                    "errors": [{
                        "kind": "NotFound",
                        "entity": f"Sample with namespace '{organization}/{namespace}' and name '{name}'",
                        "message": f"Sample with namespace '{organization}/{namespace}' and name '{name}' not found."
                    }]
                }
            )
        
        return create_sample_from_row(row)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sample {organization}/{namespace}/{name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/by/{field}/count", response_model=CountResults)
async def get_samples_count_by_field(
    field: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Group samples by the specified field and return counts."""
    try:
        df = data_loader.samples_df
        if df.empty:
            return CountResults(
                summary=EntitySummary(counts=EntityCounts(all=0, current=0)),
                data=[]
            )
        
        # Check if field is supported
        supported_fields = [
            'disease_phase', 'anatomical_sites', 'library_strategy', 
            'tissue_type', 'tumor_classification', 'preservation_method',
            'library_source_material', 'diagnosis'
        ]
        if field not in supported_fields:
            raise HTTPException(
                status_code=422,
                detail={
                    "errors": [{
                        "kind": "UnsupportedField",
                        "field": field,
                        "reason": "This field is not present for samples.",
                        "message": f"Field '{field}' is not supported: this field is not present for samples."
                    }]
                }
            )
        
        counts = data_loader.count_by_field(df, field)
        total = sum(item['count'] for item in counts)
        
        count_results = [CountResult(name=item['name'], count=item['count']) for item in counts]
        
        return CountResults(
            summary=EntitySummary(counts=EntityCounts(all=total, current=len(count_results))),
            data=count_results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting sample counts by {field}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/summary", response_model=EntityPureSummary)
async def get_samples_summary(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get summary information for samples."""
    try:
        sample_count = len(data_loader.samples_df) if not data_loader.samples_df.empty else 0
        
        return EntityPureSummary(counts=EntityPureCounts(total=sample_count))
        
    except Exception as e:
        logger.error(f"Error getting samples summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# Experimental endpoint for diagnosis search
@router.get("-diagnosis", response_model=SamplesResponse)
async def get_samples_by_diagnosis(
    data_loader: DataLoader = Depends(get_data_loader),
    search: Optional[str] = Query(None, description="Search term for diagnosis"),
    disease_phase: Optional[str] = Query(None, description="Filter by disease phase"),
    anatomical_sites: Optional[str] = Query(None, description="Filter by anatomical sites"),
    library_selection_method: Optional[str] = Query(None, description="Filter by library selection method"),
    library_strategy: Optional[str] = Query(None, description="Filter by library strategy"),
    library_source_material: Optional[str] = Query(None, description="Filter by library source material"),
    preservation_method: Optional[str] = Query(None, description="Filter by preservation method"),
    specimen_molecular_analyte_type: Optional[str] = Query(None, description="Filter by specimen molecular analyte type"),
    tissue_type: Optional[str] = Query(None, description="Filter by tissue type"),
    tumor_classification: Optional[str] = Query(None, description="Filter by tumor classification"),
    age_at_diagnosis: Optional[str] = Query(None, description="Filter by age at diagnosis"),
    age_at_collection: Optional[str] = Query(None, description="Filter by age at collection"),
    tumor_tissue_morphology: Optional[str] = Query(None, description="Filter by tumor tissue morphology"),
    depositions: Optional[str] = Query(None, description="Filter by depositions"),
    diagnosis: Optional[str] = Query(None, description="Filter by diagnosis"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, description="Number of results per page")
):
    """Experimental: Filter samples by free-text diagnosis search."""
    try:
        df = data_loader.samples_df
        if df.empty:
            page_info = PageInfo(
                page=page,
                per_page=per_page,
                total_pages=0,
                total_count=0
            )
            return SamplesResponse(
                summary=EntitySummary(counts=EntityCounts(all=0, current=0)),
                page_info=page_info,
                data=[]
            )
        
        # Apply diagnosis search filter (case-insensitive contains)
        if search:
            diagnosis_mask = df['diagnosis'].str.contains(search, case=False, na=False)
            df = df[diagnosis_mask]
        
        # Apply other filters
        filters = {
            'disease_phase': disease_phase,
            'anatomical_sites': anatomical_sites,
            'library_selection_method': library_selection_method,
            'library_strategy': library_strategy,
            'library_source_material': library_source_material,
            'preservation_method': preservation_method,
            'specimen_molecular_analyte_type': specimen_molecular_analyte_type,
            'tissue_type': tissue_type,
            'tumor_classification': tumor_classification,
            'age_at_diagnosis': age_at_diagnosis,
            'age_at_collection': age_at_collection,
            'tumor_tissue_morphology': tumor_tissue_morphology,
            'diagnosis': diagnosis
        }
        
        filtered_df = data_loader.filter_dataframe(df, filters)
        total_count = len(filtered_df)
        # Calculate pagination
        total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 0
        page_info = PageInfo(
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            total_count=total_count
        )
        
        # Apply pagination
        paginated_df = data_loader.paginate_dataframe(filtered_df, page, per_page)
        
        # Convert to Sample models
        samples = []
        for _, row in paginated_df.iterrows():
            try:
                sample = create_sample_from_row(row.to_dict())
                samples.append(sample)
            except Exception as e:
                logger.warning(f"Failed to create sample from row: {e}")
        
        return SamplesResponse(
            summary=EntitySummary(counts=EntityCounts(all=total_count, current=len(samples))),
            page_info=page_info,
            data=samples
        )
        
    except Exception as e:
        logger.error(f"Error getting samples by diagnosis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
