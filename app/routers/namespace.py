"""
Namespace router for CCDI API.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
import logging

from app.models import (
    Namespace, NamespaceIdentifier, NamespaceMetadata, MetadataField
)
from app.services.data_loader import DataLoader

logger = logging.getLogger(__name__)
router = APIRouter()


def get_data_loader(request: Request) -> DataLoader:
    """Dependency to get the data loader from app state."""
    return request.app.state.data_loader


def create_namespace_from_row(row: dict) -> Namespace:
    """Create a Namespace model from a DataFrame row."""
    # Create namespace identifier
    namespace_id = NamespaceIdentifier(
        organization=row.get('organization', ''),
        name=row.get('name', '')
    )
    
    # Create metadata
    metadata = NamespaceMetadata()
    
    if row.get('study_short_title'):
        metadata.study_short_title = MetadataField(value=row['study_short_title'])
    
    if row.get('study_name'):
        metadata.study_name = MetadataField(value=row['study_name'])
    
    if row.get('study_id'):
        metadata.study_id = MetadataField(value=row['study_id'])
    
    return Namespace(
        id=namespace_id,
        description=row.get('description', ''),
        contact_email=row.get('contact_email', ''),
        metadata=metadata
    )


@router.get("", response_model=List[Namespace])
async def get_namespaces(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get namespaces known by this server."""
    try:
        df = data_loader.namespaces_df
        if df.empty:
            return []
        
        # Convert to Namespace models
        namespaces = []
        for _, row in df.iterrows():
            try:
                namespace = create_namespace_from_row(row.to_dict())
                namespaces.append(namespace)
            except Exception as e:
                logger.warning(f"Failed to create namespace from row: {e}")
        
        return namespaces
        
    except Exception as e:
        logger.error(f"Error getting namespaces: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{organization}/{namespace}", response_model=Namespace)
async def get_namespace(
    organization: str,
    namespace: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get the namespace matching the provided name (if it exists)."""
    try:
        row = data_loader.get_namespace_by_id(organization, namespace)
        if not row:
            raise HTTPException(
                status_code=404,
                detail={
                    "errors": [{
                        "kind": "NotFound",
                        "entity": "Namespaces",
                        "message": "Namespaces not found."
                    }]
                }
            )
        
        return create_namespace_from_row(row)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting namespace {organization}/{namespace}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
