"""
Metadata router for CCDI API.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
import logging

from app.models import MetadataFieldDescriptions, HarmonizedFieldDescription, Standard
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
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#sex",
                standard=Standard(
                    name="caDSR CDE 6343385 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6343385%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="race",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#race",
                standard=Standard(
                    name="caDSR CDE 2192199 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2192199%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="ethnicity",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#ethnicity",
                standard=Standard(
                    name="caDSR CDE 2192217 v2.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2192217%20and%20ver_nr=2"
                )
            ),
            HarmonizedFieldDescription(
                path="identifiers",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#identifiers",
                standard=Standard(
                    name="caDSR CDE 6380049 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6380049%20and%20ver_nr=1"
                )

            ),
            HarmonizedFieldDescription(
                path="vital_status",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#vital_status",
                standard=Standard(
                    name="caDSR CDE 2847330 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=2847330%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="age_at_vital_status",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#age_at_vital_status",
                standard=Standard(
                    name="caDSR CDE 5432687 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5432687%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="associated_diagnoses",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#associated_diagnoses",
                standard=Standard(
                    name="caDSR CDE 5432687 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5432687%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="depositions",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Subject-Metadata-Fields#depositions",
                standard=Standard(
                    name="caDSR CDE 11524544 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11524544%20and%20ver_nr=1"
                )
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
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#disease_phase",
                standard=Standard(
                    name="caDSR CDE 12217251 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=12217251%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="anatomical_sites",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#anatomical_sites",
                standard=None
            ),
            HarmonizedFieldDescription(
                path="library_selection_method",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#library_selection_method",
                standard=Standard(
                    name="caDSR CDE 6347743 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6347743%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="library_strategy",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#library_strategy",
                standard=Standard(
                    name="caDSR CDE 6273393 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=6273393%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="library_source_material",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#library_source_material",
                standard=Standard(
                    name="caDSR CDE 15235975 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=15235975%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="preservation_method",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#preservation_method",
                standard=Standard(
                    name="caDSR CDE 8028962 v2.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=8028962%20and%20ver_nr=2"
                )
            ),
            HarmonizedFieldDescription(
                path="tumor_grade",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#tumor_grade",
                standard=Standard(
                    name="caDSR CDE 11325685 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11325685%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="specimen_molecular_analyte_type",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#specimen_molecular_analyte_type",
                standard=Standard(
                    name="caDSR CDE 15063661 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=15063661%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="tissue_type",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#tissue_type",
                standard=Standard(
                    name="caDSR CDE 14688604 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=14688604%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="tumor_classification",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#tumor_classification",
                standard=Standard(
                    name="caDSR CDE 12922545 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=12922545%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="age_at_diagnosis",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#age_at_diagnosis",
                standard=None
            ),
            HarmonizedFieldDescription(
                path="age_at_collection",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#age_at_collection",
                standard=None
            ),
            HarmonizedFieldDescription(
                path="tumor_tissue_morphology",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#tumor_tissue_morphology",
                standard=Standard(
                    name="caDSR CDE 11326261 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11326261%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="depositions",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#depositions",
                standard=Standard(
                    name="caDSR CDE 11524544 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11524544%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="diagnosis",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/Sample-Metadata-Fields#diagnosis",
                standard=Standard(
                    name="caDSR CDE 5432687 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=5432687%20and%20ver_nr=1"
                )
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
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#type",
                standard=Standard(
                    name="caDSR CDE 11416926 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11416926%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="size",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#size",
                standard=Standard(
                    name="caDSR CDE 11479876 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11479876%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="checksums",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#checksumsmd5",
                standard=Standard(
                    name="caDSR CDE 11556150 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11556150%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="description",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#description",
                standard=Standard(
                    name="caDSR CDE 11280338 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11280338%20and%20ver_nr=1"
                )
            ),
            HarmonizedFieldDescription(
                path="depositions",
                wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki/File-Metadata-Fields#depositions",
                standard=Standard(
                    name="caDSR CDE 11524544 v1.00",
                    url="https://cadsr.cancer.gov/onedata/dmdirect/NIH/NCI/CO/CDEDD?filter=CDEDD.ITEM_ID=11524544%20and%20ver_nr=1"
                )
            )
        ]
        
        return MetadataFieldDescriptions(fields=fields)
        
    except Exception as e:
        logger.error(f"Error getting file fields: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
