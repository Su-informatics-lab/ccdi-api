"""
File router for CCDI API.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import Optional
import logging

from app.models import (
    File, FilesResponse, EntitySummary, EntityCounts, CountResults, CountResult,
    FileIdentifier, SampleIdentifier, NamespaceIdentifier, MetadataField, FileMetadata, FileChecksum
)
from app.services.data_loader import DataLoader

logger = logging.getLogger(__name__)
router = APIRouter()


def get_data_loader(request: Request) -> DataLoader:
    """Dependency to get the data loader from app state."""
    return request.app.state.data_loader


def create_file_from_row(row: dict) -> File:
    """Create a File model from a DataFrame row."""
    # Create namespace identifier
    namespace = NamespaceIdentifier(
        organization=row.get('namespace_organization', ''),
        name=row.get('namespace_name', '')
    )
    
    # Create file identifier
    file_id = FileIdentifier(
        namespace=namespace,
        name=row.get('file_name', '')
    )
    
    # Create sample namespace identifier
    sample_namespace = NamespaceIdentifier(
        organization=row.get('sample_namespace_organization', ''),
        name=row.get('sample_namespace_name', '')
    )
    
    # Create sample identifiers (support multiple samples)
    sample_names = row.get('sample_names', '')
    if isinstance(sample_names, str) and sample_names:
        sample_names_list = [name.strip() for name in sample_names.split(',')]
    else:
        sample_names_list = [sample_names] if sample_names else []
    
    samples = []
    for sample_name in sample_names_list:
        if sample_name:
            sample_id = SampleIdentifier(
                namespace=sample_namespace,
                name=sample_name
            )
            samples.append(sample_id)
    
    # Create metadata fields
    metadata = FileMetadata()
    
    if row.get('type'):
        metadata.type = MetadataField(value=row['type'])
    
    if row.get('size'):
        metadata.size = MetadataField(value=int(row['size']) if str(row['size']).isdigit() else row['size'])
    
    if row.get('md5_checksum'):
        checksum = FileChecksum(md5=row['md5_checksum'])
        metadata.checksums = MetadataField(value=checksum)
    
    if row.get('description'):
        metadata.description = MetadataField(value=row['description'])
    
    return File(
        id=file_id,
        samples=samples,
        metadata=metadata
    )


@router.get("", response_model=FilesResponse)
async def get_files(
    data_loader: DataLoader = Depends(get_data_loader),
    type: Optional[str] = Query(None, description="Filter by file type"),
    size: Optional[str] = Query(None, description="Filter by file size"),
    checksums: Optional[str] = Query(None, description="Filter by checksums"),
    description: Optional[str] = Query(None, description="Filter by description (substring match)"),
    depositions: Optional[str] = Query(None, description="Filter by depositions"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(100, ge=1, description="Number of results per page")
):
    """Get files with optional filtering and pagination."""
    try:
        df = data_loader.files_df
        if df.empty:
            return FilesResponse(
                summary=EntitySummary(counts=EntityCounts(total=0)),
                data=[]
            )
        
        # Apply filters
        filtered_df = df.copy()
        
        # Standard exact match filters
        if type:
            filtered_df = filtered_df[filtered_df['type'] == type]
        if size:
            filtered_df = filtered_df[filtered_df['size'].astype(str) == size]
        if checksums:
            filtered_df = filtered_df[filtered_df['md5_checksum'] == checksums]
        
        # Description uses substring match
        if description:
            filtered_df = filtered_df[filtered_df['description'].str.contains(description, case=False, na=False)]
        
        total_count = len(filtered_df)
        
        # Apply pagination
        paginated_df = data_loader.paginate_dataframe(filtered_df, page, per_page)
        
        # Convert to File models
        files = []
        for _, row in paginated_df.iterrows():
            try:
                file_obj = create_file_from_row(row.to_dict())
                files.append(file_obj)
            except Exception as e:
                logger.warning(f"Failed to create file from row: {e}")
        
        return FilesResponse(
            summary=EntitySummary(counts=EntityCounts(total=total_count)),
            data=files
        )
        
    except Exception as e:
        logger.error(f"Error getting files: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{organization}/{namespace}/{name}", response_model=File)
async def get_file(
    organization: str,
    namespace: str,
    name: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get a specific file by identifier."""
    try:
        row = data_loader.get_file_by_id(organization, namespace, name)
        if not row:
            raise HTTPException(
                status_code=404,
                detail={
                    "errors": [{
                        "kind": "NotFound",
                        "entity": f"File with namespace '{organization}/{namespace}' and name '{name}'",
                        "message": f"File with namespace '{organization}/{namespace}' and name '{name}' not found."
                    }]
                }
            )
        
        return create_file_from_row(row)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting file {organization}/{namespace}/{name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/by/{field}/count", response_model=CountResults)
async def get_files_count_by_field(
    field: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Group files by the specified field and return counts."""
    try:
        df = data_loader.files_df
        if df.empty:
            return CountResults(
                summary=EntitySummary(counts=EntityCounts(total=0)),
                data=[]
            )
        
        # Check if field is supported
        supported_fields = ['type', 'size']
        if field not in supported_fields:
            raise HTTPException(
                status_code=422,
                detail={
                    "errors": [{
                        "kind": "UnsupportedField",
                        "field": field,
                        "reason": "This field is not present for files.",
                        "message": f"Field '{field}' is not supported: this field is not present for files."
                    }]
                }
            )
        
        counts = data_loader.count_by_field(df, field)
        total = sum(item['count'] for item in counts)
        
        count_results = [CountResult(name=item['name'], count=item['count']) for item in counts]
        
        return CountResults(
            summary=EntitySummary(counts=EntityCounts(total=total)),
            data=count_results
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting file counts by {field}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/summary", response_model=EntitySummary)
async def get_files_summary(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get summary information for files."""
    try:
        file_count = len(data_loader.files_df) if not data_loader.files_df.empty else 0
        
        return EntitySummary(counts=EntityCounts(total=file_count))
        
    except Exception as e:
        logger.error(f"Error getting files summary: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
