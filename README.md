# CCDI Data Federation API

FastAPI implementation of the CCDI Data Federation Participating Nodes API.

## Overview

This is a Python FastAPI server that implements the CCDI (Childhood Cancer Data Initiative) Data Federation API specification. The server loads data from CSV files into pandas DataFrames and provides REST endpoints for querying subjects, samples, files, metadata, namespaces, and organizations.

## Features

- ✅ Full implementation of CCDI API v1.2.0 specification
- ✅ FastAPI with automatic OpenAPI/Swagger documentation
- ✅ CSV data loading with pandas
- ✅ In-memory data querying and filtering
- ✅ Pagination support
- ✅ Comprehensive error handling
- ✅ Sample data generation
- ✅ CORS support

## API Endpoints

### Core Entities
- **Subjects**: `/subject` - Patient/participant data
- **Samples**: `/sample` - Biological sample data  
- **Files**: `/file` - Data file information
- **Metadata**: `/metadata` - Field descriptions
- **Namespaces**: `/namespace` - Study/project namespaces
- **Organizations**: `/organization` - Institution data
- **Info**: `/info` - Server information

### Features
- List endpoints with filtering and pagination
- Individual entity retrieval
- Count aggregation by field
- Summary statistics
- Experimental diagnosis search

## Quick Start

1. **Install dependencies**:
   ```bash
   # Dependencies are already installed via uv
   ```

2. **Start the server**:
   ```bash
   uv run python start.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - OpenAPI spec: http://localhost:8000/openapi.json

## Data Files

The server expects CSV files in the `data/` directory:

- `subjects.csv` - Subject/participant data
- `samples.csv` - Biological sample data
- `files.csv` - File metadata
- `namespaces.csv` - Study/project information
- `organizations.csv` - Institution data

Sample data files are automatically created on first run if they don't exist.

## CSV Schema

### subjects.csv
```csv
namespace_organization,namespace_name,subject_name,kind,sex,race,ethnicity,vital_status,age_at_vital_status,associated_diagnoses
STJUDE,PNOC,SUBJECT001,Participant,F,White,Not Hispanic or Latino,Alive,2555,Acute Lymphoblastic Leukemia
```

### samples.csv
```csv
namespace_organization,namespace_name,sample_name,subject_namespace_organization,subject_namespace_name,subject_name,disease_phase,tissue_type,tumor_classification,anatomical_sites,library_strategy,library_source_material,preservation_method,diagnosis,age_at_diagnosis,age_at_collection
STJUDE,PNOC,SAMPLE001,STJUDE,PNOC,SUBJECT001,Initial Diagnosis,Tumor,Primary,Brain,RNA-Seq,Bulk Tissue,Fresh,Acute Lymphoblastic Leukemia,2555,2600
```

### files.csv
```csv
namespace_organization,namespace_name,file_name,sample_namespace_organization,sample_namespace_name,sample_names,type,size,md5_checksum,description
STJUDE,PNOC,RNASeq_001.fastq.gz,STJUDE,PNOC,SAMPLE001,FASTQ,1073741824,d41d8cd98f00b204e9800998ecf8427e,RNA sequencing raw reads
```

### namespaces.csv
```csv
organization,name,description,contact_email,study_short_title,study_name,study_id
STJUDE,PNOC,Pediatric Neuro-Oncology Consortium,pnoc@stjude.org,PNOC Study,Pediatric Neuro-Oncology Consortium Study,PNOC001
```

### organizations.csv
```csv
identifier,name,institution
STJUDE,St. Jude Children's Research Hospital,SJCRH
```

## API Examples

### Get all subjects with pagination
```bash
curl "http://localhost:8000/subject?page=1&per_page=10"
```

### Filter subjects by sex
```bash
curl "http://localhost:8000/subject?sex=F"
```

### Get a specific subject
```bash
curl "http://localhost:8000/subject/STJUDE/PNOC/SUBJECT001"
```

### Search samples by diagnosis
```bash
curl "http://localhost:8000/sample-diagnosis?search=leukemia"
```

### Get count by field
```bash
curl "http://localhost:8000/subject/by/sex/count"
```

### Get summary statistics
```bash
curl "http://localhost:8000/subject/summary"
```

## Development

### Project Structure
```
ccdi-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── models/
│   │   └── __init__.py      # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── subject.py       # Subject endpoints
│   │   ├── sample.py        # Sample endpoints
│   │   ├── file.py          # File endpoints
│   │   ├── metadata.py      # Metadata endpoints
│   │   ├── namespace.py     # Namespace endpoints
│   │   ├── organization.py  # Organization endpoints
│   │   └── info.py          # Info endpoints
│   └── services/
│       ├── __init__.py
│       └── data_loader.py   # CSV data loading service
├── data/                    # CSV data files
├── start.py                 # Start script
├── swagger.yml              # Original API specification
├── pyproject.toml          # uv project configuration
└── README.md               # This file
```

### Adding Custom Data

1. Replace the CSV files in the `data/` directory with your own data
2. Restart the server to reload the data
3. The server will automatically detect and load the new data

### Extending the API

- Add new endpoints in the appropriate router files
- Extend the Pydantic models for new data fields
- Update the data loader service for new data sources
- Follow the existing patterns for error handling and response formatting

## Configuration

The server can be configured via environment variables or by modifying the configuration in `app/main.py`:

- **Host**: Default `0.0.0.0`
- **Port**: Default `8000`
- **Data Directory**: Default `data/`
- **Log Level**: Default `info`

## Error Handling

The API follows the CCDI specification for error responses:

```json
{
  "errors": [
    {
      "kind": "NotFound",
      "entity": "Subject with namespace 'ORG/NS' and name 'NAME'",
      "message": "Subject not found."
    }
  ]
}
```

## Standards Compliance

This implementation follows:
- CCDI Data Federation API v1.2.0 specification
- OpenAPI 3.0.3 standard
- RESTful API design principles
- JSON response formatting
- Standard HTTP status codes

## License

This project implements the CCDI Data Federation API specification.
