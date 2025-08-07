"""
Metadata router for CCDI API.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
import logging

from app.models import FieldDescriptions, FieldDescription
from app.services.data_loader import DataLoader

logger = logging.getLogger(__name__)
router = APIRouter()


def get_data_loader(request: Request) -> DataLoader:
    """Dependency to get the data loader from app state."""
    return request.app.state.data_loader


@router.get("/fields/subject", response_model=FieldDescriptions)
async def get_subject_fields(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get metadata fields for subjects that are supported by this server."""
    try:
        fields = [
            FieldDescription(
                name="sex",
                description="The sex of the subject",
                required=False
            ),
            FieldDescription(
                name="race",
                description="The race(s) of the subject",
                required=False
            ),
            FieldDescription(
                name="ethnicity", 
                description="The ethnicity of the subject",
                required=False
            ),
            FieldDescription(
                name="identifiers",
                description="Alternative identifiers for the subject",
                required=False
            ),
            FieldDescription(
                name="vital_status",
                description="The vital status of the subject",
                required=False
            ),
            FieldDescription(
                name="age_at_vital_status",
                description="Age at vital status determination",
                required=False
            ),
            FieldDescription(
                name="associated_diagnoses",
                description="Diagnoses associated with the subject",
                required=False
            ),
            FieldDescription(
                name="depositions",
                description="Data depositions associated with the subject",
                required=False
            )
        ]
        
        return FieldDescriptions(fields=fields)
        
    except Exception as e:
        logger.error(f"Error getting subject fields: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/fields/sample", response_model=FieldDescriptions)
async def get_sample_fields(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get metadata fields for samples that are supported by this server."""
    try:
        fields = [
            FieldDescription(
                name="disease_phase",
                description="The phase of disease when the sample was collected",
                required=False
            ),
            FieldDescription(
                name="anatomical_sites",
                description="Anatomical site(s) where the sample was collected",
                required=False
            ),
            FieldDescription(
                name="library_selection_method",
                description="The method used to select library fragments",
                required=False
            ),
            FieldDescription(
                name="library_strategy",
                description="The overall strategy for library construction",
                required=False
            ),
            FieldDescription(
                name="library_source_material",
                description="The source material for library construction",
                required=False
            ),
            FieldDescription(
                name="preservation_method",
                description="The method used to preserve the sample",
                required=False
            ),
            FieldDescription(
                name="tumor_grade",
                description="The grade of the tumor sample",
                required=False
            ),
            FieldDescription(
                name="specimen_molecular_analyte_type",
                description="The type of molecular analyte in the specimen",
                required=False
            ),
            FieldDescription(
                name="tissue_type",
                description="The type of tissue in the sample",
                required=False
            ),
            FieldDescription(
                name="tumor_classification",
                description="The classification of the tumor",
                required=False
            ),
            FieldDescription(
                name="age_at_diagnosis",
                description="Age at diagnosis",
                required=False
            ),
            FieldDescription(
                name="age_at_collection",
                description="Age when the sample was collected",
                required=False
            ),
            FieldDescription(
                name="tumor_tissue_morphology",
                description="Morphology of the tumor tissue",
                required=False
            ),
            FieldDescription(
                name="depositions",
                description="Data depositions associated with the sample",
                required=False
            ),
            FieldDescription(
                name="diagnosis",
                description="The diagnosis associated with the sample",
                required=False
            )
        ]
        
        return FieldDescriptions(fields=fields)
        
    except Exception as e:
        logger.error(f"Error getting sample fields: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/fields/file", response_model=FieldDescriptions)
async def get_file_fields(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get metadata fields for files that are supported by this server."""
    try:
        fields = [
            FieldDescription(
                name="type",
                description="The type/format of the file",
                required=False
            ),
            FieldDescription(
                name="size",
                description="The size of the file in bytes",
                required=False
            ),
            FieldDescription(
                name="checksums",
                description="Checksums for file integrity verification",
                required=False
            ),
            FieldDescription(
                name="description",
                description="A description of the file contents",
                required=False
            ),
            FieldDescription(
                name="depositions",
                description="Data depositions associated with the file",
                required=False
            )
        ]
        
        return FieldDescriptions(fields=fields)
        
    except Exception as e:
        logger.error(f"Error getting file fields: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
