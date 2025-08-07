"""
Organization router for CCDI API.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
import logging

from app.models import (
    Organization, OrganizationMetadata, MetadataField
)
from app.services.data_loader import DataLoader

logger = logging.getLogger(__name__)
router = APIRouter()


def get_data_loader(request: Request) -> DataLoader:
    """Dependency to get the data loader from app state."""
    return request.app.state.data_loader


def create_organization_from_row(row: dict) -> Organization:
    """Create an Organization model from a DataFrame row."""
    # Create metadata
    metadata = OrganizationMetadata()
    
    if row.get('institution'):
        metadata.institution = [MetadataField(value=row['institution'])]
    
    return Organization(
        identifier=row.get('identifier', ''),
        name=row.get('name', ''),
        metadata=metadata
    )


@router.get("", response_model=List[Organization])
async def get_organizations(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get organizations known by this server."""
    try:
        df = data_loader.organizations_df
        if df.empty:
            return []
        
        # Convert to Organization models
        organizations = []
        for _, row in df.iterrows():
            try:
                organization = create_organization_from_row(row.to_dict())
                organizations.append(organization)
            except Exception as e:
                logger.warning(f"Failed to create organization from row: {e}")
        
        return organizations
        
    except Exception as e:
        logger.error(f"Error getting organizations: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{name}", response_model=Organization)
async def get_organization(
    name: str,
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get the organization matching the provided name (if it exists)."""
    try:
        row = data_loader.get_organization_by_name(name)
        if not row:
            raise HTTPException(
                status_code=404,
                detail={
                    "errors": [{
                        "kind": "NotFound",
                        "entity": "Organization",
                        "message": "Organization not found."
                    }]
                }
            )
        
        return create_organization_from_row(row)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting organization {name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
