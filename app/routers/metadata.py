"""
Metadata router for CCDI API.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
import logging

from app.models import MetadataFieldDescriptions, HarmonizedFieldDescription
from app.services.data_loader import DataLoader

logger = logging.getLogger(__name__)
router = APIRouter()


def get_data_loader(request: Request) -> DataLoader:
    """Dependency to get the data loader from app state."""
    return request.app.state.data_loader


@router.get("/fields/subject", response_model=MetadataFieldDescriptions)
async def get_subject_fields(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get metadata fields for subjects that are supported by this server."""
    try:
        fields = [
            HarmonizedFieldDescription(
                path="sex",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#sex"
            ),
            HarmonizedFieldDescription(
                path="race",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#race"
            ),
            HarmonizedFieldDescription(
                path="ethnicity",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#ethnicity"
            ),
            HarmonizedFieldDescription(
                path="identifiers",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#identifiers"
            ),
            HarmonizedFieldDescription(
                path="vital_status",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#vital_status"
            ),
            HarmonizedFieldDescription(
                path="age_at_vital_status",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#age_at_vital_status"
            ),
            HarmonizedFieldDescription(
                path="associated_diagnoses",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#associated_diagnoses"
            ),
            HarmonizedFieldDescription(
                path="depositions",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#depositions"
            )
        ]
        
        return MetadataFieldDescriptions(fields=fields)
        
    except Exception as e:
        logger.error(f"Error getting subject fields: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/fields/sample", response_model=MetadataFieldDescriptions)
async def get_sample_fields(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get metadata fields for samples that are supported by this server."""
    try:
        fields = [
            HarmonizedFieldDescription(
                path="disease_phase",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#disease_phase"
            ),
            HarmonizedFieldDescription(
                path="anatomical_sites",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#anatomical_sites"
            ),
            HarmonizedFieldDescription(
                path="library_selection_method",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#library_selection_method"
            ),
            HarmonizedFieldDescription(
                path="library_strategy",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#library_strategy"
            ),
            HarmonizedFieldDescription(
                path="library_source_material",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#library_source_material"
            ),
            HarmonizedFieldDescription(
                path="preservation_method",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#preservation_method"
            ),
            HarmonizedFieldDescription(
                path="tumor_grade",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#tumor_grade"
            ),
            HarmonizedFieldDescription(
                path="specimen_molecular_analyte_type",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#specimen_molecular_analyte_type"
            ),
            HarmonizedFieldDescription(
                path="tissue_type",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#tissue_type"
            ),
            HarmonizedFieldDescription(
                path="tumor_classification",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#tumor_classification"
            ),
            HarmonizedFieldDescription(
                path="age_at_diagnosis",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#age_at_diagnosis"
            ),
            HarmonizedFieldDescription(
                path="age_at_collection",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#age_at_collection"
            ),
            HarmonizedFieldDescription(
                path="tumor_tissue_morphology",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#tumor_tissue_morphology"
            ),
            HarmonizedFieldDescription(
                path="depositions",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#depositions"
            ),
            HarmonizedFieldDescription(
                path="diagnosis",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#diagnosis"
            )
        ]
        
        return MetadataFieldDescriptions(fields=fields)
        
    except Exception as e:
        logger.error(f"Error getting sample fields: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/fields/file", response_model=MetadataFieldDescriptions)
async def get_file_fields(
    data_loader: DataLoader = Depends(get_data_loader)
):
    """Get metadata fields for files that are supported by this server."""
    try:
        fields = [
            HarmonizedFieldDescription(
                path="type",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#type"
            ),
            HarmonizedFieldDescription(
                path="size",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#size"
            ),
            HarmonizedFieldDescription(
                path="checksums",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#checksumsmd5"
            ),
            HarmonizedFieldDescription(
                path="description",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#description"
            ),
            # HarmonizedFieldDescription(
            #     path="depositions",
            #     wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#depositions"
            # )
        ]
        
        return MetadataFieldDescriptions(fields=fields)
        
    except Exception as e:
        logger.error(f"Error getting file fields: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
