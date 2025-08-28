"""
Pydantic models for CCDI API based on the OpenAPI specification.
"""

from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field, RootModel
from enum import Enum


# Enums based on the swagger specification
class SubjectSex(str, Enum):
    U = "U"
    F = "F"
    M = "M"
    UNDIFFERENTIATED = "UNDIFFERENTIATED"


class SubjectRace(str, Enum):
    NOT_ALLOWED = "Not allowed to collect"
    PACIFIC_ISLANDER = "Native Hawaiian or other Pacific Islander"
    NOT_REPORTED = "Not Reported"
    UNKNOWN = "Unknown"
    AMERICAN_INDIAN = "American Indian or Alaska Native"
    ASIAN = "Asian"
    BLACK = "Black or African American"
    WHITE = "White"


class SubjectEthnicity(str, Enum):
    NOT_REPORTED = "Not reported"
    HISPANIC = "Hispanic or Latino"
    NOT_HISPANIC = "Not Hispanic or Latino"
    UNKNOWN = "Unknown"


class SubjectVitalStatus(str, Enum):
    NOT_REPORTED = "Not reported"
    ALIVE = "Alive"
    DEAD = "Dead"
    UNKNOWN = "Unknown"
    UNSPECIFIED = "Unspecified"


class SubjectKind(str, Enum):
    PARTICIPANT = "Participant"
    PDX = "Patient Derived Xenograft"
    CELL_LINE = "Cell Line"
    ORGANOID = "Organoid"


class SampleDiseasePhase(str, Enum):
    POST_MORTEM = "Post-Mortem"
    NOT_REPORTED = "Not Reported"
    UNKNOWN = "Unknown"
    INITIAL_DIAGNOSIS = "Initial Diagnosis"
    PROGRESSION = "Progression"
    REFRACTORY = "Refractory"
    RELAPSE = "Relapse"
    RELAPSE_PROGRESSION = "Relapse/Progression"


class SampleTissueType(str, Enum):
    NOT_REPORTED = "Not Reported"
    NORMAL = "Normal"
    PERITUMORAL = "Peritumoral"
    TUMOR = "Tumor"
    UNKNOWN = "Unknown"


class SampleTumorClassification(str, Enum):
    METASTATIC = "Metastatic"
    NOT_REPORTED = "Not Reported"
    PRIMARY = "Primary"
    REGIONAL = "Regional"
    UNKNOWN = "Unknown"


class FileType(str, Enum):
    ADF = "ADF"
    AVI = "AVI"
    BAI = "BAI"
    BAM = "BAM"
    BCR_BIOTAB = "BCR Biotab"
    BED = "BED"
    BEDGRAPH = "bedgraph"
    BEDPE = "BEDPE Format"
    BIGBED = "bigBed"
    BIGWIG = "bigWig"
    BINARY = "Binary Format"
    BIOM = "BIOM"
    CDF = "cdf"
    CEL = "CEL"
    CNS = "CNS"
    CRAI = "CRAI"
    CRAM = "CRAM"
    CSV = "CSV"
    DICOM = "DICOM"
    DICT = "DICT"
    DOC = "DOC"
    DOCX = "DOCX"
    DSV = "DSV"
    FASTA = "FASTA"
    FASTQ = "FASTQ"
    GCT = "GCT/Res Format"
    GENBANK = "GenBank Format"
    GFF3 = "GFF3"
    GPR = "GPR"
    GTF = "GTF"
    GVCF = "gVCF"
    GZIP = "GZIP Format"
    HDF5 = "HDF5"
    HIC = "HIC"
    HTML = "HTML"
    HTSEQ = "HTSeq Count"
    IDAT = "IDAT"
    IDF = "IDF"
    IDPDB = "idpDB"
    JPEG = "JPEG"
    JPEG2000 = "JPEG 2000"
    JSON = "JSON"
    MAF = "MAF"
    MAGE_TAB = "MAGE-TAB"
    MAT = "MAT"
    MATLAB = "MATLAB Script"
    MEX = "MEX"
    MPEG4 = "MPEG-4"
    MTX = "mtx"
    MZIDENTML = "mzIdentML"
    MZML = "mzML"
    MZXML = "mzXML"
    NIFTI = "NIFTI Format"
    OME_TIFF = "OME-TIFF"
    PDF = "PDF"
    PED = "PED"
    PLAIN_TEXT = "Plain Text Data Format"
    PNG = "PNG"
    PYTHON = "Python Script Format"
    R_FILE = "R File Format"
    R_MARKDOWN = "R Markdown"
    RDS = "rds"
    RTF = "RTF"
    SDRF = "SDRF"
    SEG = "SEG"
    SEQUENCE = "Sequence Record Format"
    SVG = "SVG"
    SVS = "SVS"
    TAR = "TAR"
    TBI = "TBI"
    THERMO_RAW = "Thermo RAW"
    TIFF = "TIFF"
    TSV = "TSV"
    TXT = "TXT"
    VCF = "VCF"
    XLS = "XLS"
    XLSX = "XLSX"
    XML = "XML"
    YAML = "YAML"
    ZIP = "ZIP"


# Base identifier models
class NamespaceIdentifier(BaseModel):
    organization: str = Field(..., description="The organization identifier")
    name: str = Field(..., description="The namespace name")


class SubjectIdentifier(BaseModel):
    namespace: NamespaceIdentifier
    name: str = Field(..., description="The subject name", example="SubjectName001")


class SampleIdentifier(BaseModel):
    namespace: NamespaceIdentifier
    name: str = Field(..., description="The sample name", example="SampleName001")


class FileIdentifier(BaseModel):
    namespace: NamespaceIdentifier
    name: str = Field(..., description="The file name", example="File001.txt")


# Metadata field wrapper
class MetadataField(BaseModel):
    value: Any
    ancestors: Optional[List[str]] = None
    comment: Optional[str] = None


# Subject models
class SubjectMetadata(BaseModel):
    sex: Optional[MetadataField] = None
    race: Optional[List[MetadataField]] = None
    ethnicity: Optional[MetadataField] = None
    identifiers: Optional[List[MetadataField]] = None
    vital_status: Optional[MetadataField] = None
    age_at_vital_status: Optional[MetadataField] = None
    associated_diagnoses: Optional[List[MetadataField]] = None
    depositions: Optional[List[MetadataField]] = None
    unharmonized: Optional[Dict[str, Any]] = None


class Subject(BaseModel):
    id: SubjectIdentifier
    kind: SubjectKind
    metadata: Optional[SubjectMetadata] = None


# Sample models
class SampleMetadata(BaseModel):
    disease_phase: Optional[MetadataField] = None
    anatomical_sites: Optional[List[MetadataField]] = None
    library_selection_method: Optional[MetadataField] = None
    library_strategy: Optional[MetadataField] = None
    library_source_material: Optional[MetadataField] = None
    preservation_method: Optional[MetadataField] = None
    tumor_grade: Optional[MetadataField] = None
    specimen_molecular_analyte_type: Optional[MetadataField] = None
    tissue_type: Optional[MetadataField] = None
    tumor_classification: Optional[MetadataField] = None
    age_at_diagnosis: Optional[MetadataField] = None
    age_at_collection: Optional[MetadataField] = None
    tumor_tissue_morphology: Optional[MetadataField] = None
    depositions: Optional[List[MetadataField]] = None
    diagnosis: Optional[MetadataField] = None
    identifiers: Optional[List[MetadataField]] = None
    unharmonized: Optional[Dict[str, Any]] = None


class Sample(BaseModel):
    id: SampleIdentifier
    subject: SubjectIdentifier
    metadata: Optional[SampleMetadata] = None


# File models
class FileChecksum(BaseModel):
    md5: Optional[str] = None


class FileMetadata(BaseModel):
    type: Optional[MetadataField] = None
    size: Optional[MetadataField] = None
    checksums: Optional[MetadataField] = None
    description: Optional[MetadataField] = None
    depositions: Optional[List[MetadataField]] = None
    unharmonized: Optional[Dict[str, Any]] = None


class File(BaseModel):
    id: FileIdentifier
    samples: List[SampleIdentifier]
    metadata: Optional[FileMetadata] = None


# Namespace models
class NamespaceMetadata(BaseModel):
    study_short_title: Optional[MetadataField] = None
    study_name: Optional[MetadataField] = None
    study_funding_id: Optional[List[MetadataField]] = None
    study_id: Optional[MetadataField] = None
    unharmonized: Optional[Dict[str, Any]] = None


class Namespace(BaseModel):
    id: NamespaceIdentifier
    description: str
    contact_email: str = Field(..., example="support@example.com")
    metadata: Optional[NamespaceMetadata] = None


# Organization models
class OrganizationMetadata(BaseModel):
    institution: Optional[List[MetadataField]] = None
    unharmonized: Optional[Dict[str, Any]] = None


class Organization(BaseModel):
    identifier: str
    name: str
    metadata: Optional[OrganizationMetadata] = None


# Response models
class EntitySummary(BaseModel):
    total: int = Field(..., ge=0)


class Summary(BaseModel):
    subjects: EntitySummary
    samples: EntitySummary
    files: EntitySummary


class SubjectsResponse(BaseModel):
    summary: EntitySummary
    data: List[Subject]


class SamplesResponse(BaseModel):
    summary: EntitySummary
    data: List[Sample]


class FilesResponse(BaseModel):
    summary: EntitySummary
    data: List[File]


class NamespacesResponse(RootModel[List[Namespace]]):
    root: List[Namespace]


class OrganizationsResponse(RootModel[List[Organization]]):
    root: List[Organization]


# Count response models
class CountResult(BaseModel):
    name: str
    count: int = Field(..., ge=0)


class CountResults(BaseModel):
    summary: EntitySummary
    data: List[CountResult]


# Error models
class Error(BaseModel):
    kind: str
    entity: Optional[str] = None
    field: Optional[str] = None
    reason: Optional[str] = None
    message: str


class ErrorResponse(BaseModel):
    errors: List[Error]


# Metadata field description models
class FieldDescription(BaseModel):
    name: str
    description: str
    required: bool = False


class FieldDescriptions(BaseModel):
    fields: List[FieldDescription]


# Info models
class ServerInfo(BaseModel):
    name: str
    version: str
    owner: str
    contact_email: str
    description: str


class APIInfo(BaseModel):
    api_version: str
    documentation_url: str


class VersionInfo(BaseModel):
    version: str
    about: str


class DataInfo(BaseModel):
    version: VersionInfo
    last_updated: str
    source: str
    wiki_url: str


class InfoResponse(BaseModel):
    server: ServerInfo
    api: APIInfo
    data: DataInfo


# Query parameter models
class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number (1-based)")
    per_page: int = Field(100, ge=1, description="Number of results per page")


class SubjectQueryParams(PaginationParams):
    sex: Optional[str] = None
    race: Optional[str] = None
    ethnicity: Optional[str] = None
    identifiers: Optional[str] = None
    vital_status: Optional[str] = None
    age_at_vital_status: Optional[str] = None
    depositions: Optional[str] = None


class SampleQueryParams(PaginationParams):
    disease_phase: Optional[str] = None
    anatomical_sites: Optional[str] = None
    library_selection_method: Optional[str] = None
    library_strategy: Optional[str] = None
    library_source_material: Optional[str] = None
    preservation_method: Optional[str] = None
    tumor_grade: Optional[str] = None
    specimen_molecular_analyte_type: Optional[str] = None
    tissue_type: Optional[str] = None
    tumor_classification: Optional[str] = None
    age_at_diagnosis: Optional[str] = None
    age_at_collection: Optional[str] = None
    tumor_tissue_morphology: Optional[str] = None
    depositions: Optional[str] = None
    diagnosis: Optional[str] = None


class FileQueryParams(PaginationParams):
    type: Optional[str] = None
    size: Optional[str] = None
    checksums: Optional[str] = None
    description: Optional[str] = None
    depositions: Optional[str] = None
