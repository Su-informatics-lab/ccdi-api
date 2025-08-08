# CCDI API Data Files Documentation

This directory contains CSV files that serve as the data source for the CCDI (Childhood Cancer Data Initiative) Federation API. Each file represents a different entity type in the federated data model.

## File Overview

- **organizations.csv** - Research organizations and institutions
- **namespaces.csv** - Study namespaces and research projects
- **subjects.csv** - Study participants (patients/cell lines)
- **samples.csv** - Biological samples collected from subjects
- **files.csv** - Data files associated with samples

## Column Definitions

### organizations.csv

| Column | Type | Description |
|--------|------|-------------|
| `identifier` | String | Unique identifier for the organization (e.g., "STJUDE", "COG") |
| `name` | String | Full name of the organization (e.g., "St. Jude Children's Research Hospital") |
| `institution` | String | Institution abbreviation or code (e.g., "SJCRH", "COG") |

### namespaces.csv

| Column | Type | Description |
|--------|------|-------------|
| `organization` | String | Organization identifier (foreign key to organizations.csv) |
| `name` | String | Namespace identifier within the organization (e.g., "PNOC", "AML0531") |
| `description` | String | Human-readable description of the study or namespace |
| `contact_email` | String | Contact email for the study or namespace |
| `study_short_title` | String | Short title or abbreviation for the study |
| `study_name` | String | Full name of the study |
| `study_id` | String | Unique study identifier (e.g., "PNOC001", "AAML0531") |

### subjects.csv

| Column | Type | Description |
|--------|------|-------------|
| `namespace_organization` | String | Organization identifier for the namespace |
| `namespace_name` | String | Namespace identifier |
| `subject_name` | String | Unique identifier for the subject within the namespace |
| `kind` | String | Type of subject ("Participant" for patients, "Cell Line" for cell lines) |
| `sex` | String | Biological sex ("M" = Male, "F" = Female, "U" = Unknown/Unspecified) |
| `race` | String | Race category (e.g., "White", "Asian", "Black or African American", "Not Reported") |
| `ethnicity` | String | Ethnicity category (e.g., "Not Hispanic or Latino", "Hispanic or Latino", "Unknown") |
| `vital_status` | String | Current vital status ("Alive", "Dead", "Unknown") |
| `age_at_vital_status` | Integer | Age in days at the time of vital status determination (empty for cell lines) |
| `associated_diagnoses` | String | Primary diagnosis or cancer type |

### samples.csv

| Column | Type | Description |
|--------|------|-------------|
| `namespace_organization` | String | Organization identifier for the sample's namespace |
| `namespace_name` | String | Namespace identifier for the sample |
| `sample_name` | String | Unique identifier for the sample within the namespace |
| `subject_namespace_organization` | String | Organization identifier for the associated subject |
| `subject_namespace_name` | String | Namespace identifier for the associated subject |
| `subject_name` | String | Subject identifier (foreign key to subjects.csv) |
| `disease_phase` | String | Phase of disease when sample was collected ("Initial Diagnosis", "Progression", "Relapse") |
| `tissue_type` | String | Type of tissue ("Tumor", "Normal") |
| `tumor_classification` | String | Tumor classification ("Primary", "Metastatic", "Not Reported") |
| `anatomical_sites` | String | Anatomical location where sample was collected (e.g., "Brain", "Bone Marrow") |
| `library_strategy` | String | Sequencing library strategy (e.g., "RNA-Seq", "WGS", "WXS") |
| `library_source_material` | String | Source material type ("Bulk Tissue", "Bulk Cells") |
| `preservation_method` | String | Sample preservation method ("Fresh", "FFPE", "Frozen") |
| `diagnosis` | String | Specific diagnosis for this sample |
| `age_at_diagnosis` | Integer | Age in days at time of diagnosis |
| `age_at_collection` | Integer | Age in days when sample was collected |

### files.csv

| Column | Type | Description |
|--------|------|-------------|
| `namespace_organization` | String | Organization identifier for the file's namespace |
| `namespace_name` | String | Namespace identifier for the file |
| `file_name` | String | Name of the data file |
| `sample_namespace_organization` | String | Organization identifier for the associated sample |
| `sample_namespace_name` | String | Namespace identifier for the associated sample |
| `sample_names` | String | Sample identifier (foreign key to samples.csv) |
| `type` | String | File format type (e.g., "FASTQ", "BAM", "VCF") |
| `size` | Integer | File size in bytes |
| `md5_checksum` | String | MD5 hash checksum for file integrity verification |
| `description` | String | Human-readable description of the file contents |

## Data Relationships

The data follows a hierarchical structure:

```
Organizations
├── Namespaces (Studies)
    ├── Subjects (Patients/Cell Lines)
        ├── Samples (Biological specimens)
            ├── Files (Data files)
```

## Key Notes

- **Age Values**: All age-related fields are expressed in days
- **Identifiers**: Composite keys are used (organization + namespace + entity_name) to ensure uniqueness across the federation
- **Foreign Keys**: Relationships between entities are maintained through namespace organization, namespace name, and entity identifiers
- **Data Types**: 
  - String fields may contain controlled vocabulary terms
  - Integer fields represent numeric values (ages, file sizes)
  - Empty values indicate missing or not applicable data

## Usage

These CSV files are loaded by the CCDI API's DataLoader service at startup and serve as the backend data source for all API endpoints. The data structure supports the federated nature of the CCDI initiative, allowing multiple organizations to contribute data while maintaining proper attribution and namespace separation.
