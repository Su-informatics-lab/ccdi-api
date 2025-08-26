"""
Data loader service for loading CSV data into pandas DataFrames.
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import asyncio
from functools import lru_cache

logger = logging.getLogger(__name__)


class DataLoader:
    """Service for loading and managing CSV data."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.subjects_df: Optional[pd.DataFrame] = None
        self.samples_df: Optional[pd.DataFrame] = None
        self.files_df: Optional[pd.DataFrame] = None
        self.namespaces_df: Optional[pd.DataFrame] = None
        self.organizations_df: Optional[pd.DataFrame] = None
        
    async def load_all_data(self):
        """Load all CSV data files."""
        logger.info("Loading data from CSV files...")
        
        # Create sample data if files don't exist
        await self._ensure_sample_data()
        
        # Load data files
        await asyncio.gather(
            self._load_subjects(),
            self._load_samples(),
            self._load_files(),
            self._load_namespaces(),
            self._load_organizations()
        )
        
        logger.info("All data loaded successfully")
    
    async def _ensure_sample_data(self):
        """Create sample CSV files if they don't exist."""
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)
            
        # Create sample subjects data
        subjects_file = self.data_dir / "subjects.csv"
        if not subjects_file.exists():
            subjects_data = {
                'namespace_organization': ['STJUDE', 'TREEHOUSE', 'COG', 'STJUDE', 'TREEHOUSE'],
                'namespace_name': ['PNOC', 'COMPBIO', 'AML0531', 'PNOC', 'COMPBIO'],
                'subject_name': ['SUBJECT001', 'SUBJECT002', 'SUBJECT003', 'SUBJECT004', 'SUBJECT005'],
                'kind': ['Participant', 'Participant', 'Participant', 'Cell Line', 'Organoid'],
                'sex': ['F', 'M', 'F', 'U', 'F'],
                'race': ['White', 'Asian', 'Black or African American', 'Not Reported', 'White'],
                'ethnicity': ['Not Hispanic or Latino', 'Not reported', 'Hispanic or Latino', 'Unknown', 'Not Hispanic or Latino'],
                'vital_status': ['Alive', 'Dead', 'Alive', 'Unknown', 'Alive'],
                'age_at_vital_status': ['2555', '4380', '3650', '', '1825'],
                'associated_diagnoses': ['Acute Lymphoblastic Leukemia', 'Glioblastoma', 'Acute Myeloid Leukemia', 'Neuroblastoma', 'Medulloepithelioma']
            }
            pd.DataFrame(subjects_data).to_csv(subjects_file, index=False)
            logger.info(f"Created sample subjects data: {subjects_file}")
        
        # Create sample samples data
        samples_file = self.data_dir / "samples.csv"
        if not samples_file.exists():
            samples_data = {
                'namespace_organization': ['STJUDE', 'TREEHOUSE', 'COG', 'STJUDE', 'TREEHOUSE', 'COG'],
                'namespace_name': ['PNOC', 'COMPBIO', 'AML0531', 'PNOC', 'COMPBIO', 'AML0531'],
                'sample_name': ['SAMPLE001', 'SAMPLE002', 'SAMPLE003', 'SAMPLE004', 'SAMPLE005', 'SAMPLE006'],
                'subject_namespace_organization': ['STJUDE', 'TREEHOUSE', 'COG', 'STJUDE', 'TREEHOUSE', 'COG'],
                'subject_namespace_name': ['PNOC', 'COMPBIO', 'AML0531', 'PNOC', 'COMPBIO', 'AML0531'],
                'subject_name': ['SUBJECT001', 'SUBJECT002', 'SUBJECT003', 'SUBJECT001', 'SUBJECT002', 'SUBJECT003'],
                'disease_phase': ['Initial Diagnosis', 'Progression', 'Relapse', 'Initial Diagnosis', 'Refractory', 'Progression'],
                'tissue_type': ['Tumor', 'Tumor', 'Tumor', 'Normal', 'Tumor', 'Peritumoral'],
                'tumor_classification': ['Primary', 'Metastatic', 'Primary', 'Not Reported', 'Regional', 'Primary'],
                'anatomical_sites': ['Brain', 'Brain', 'Bone Marrow', 'Brain', 'Brain', 'Bone Marrow'],
                'library_strategy': ['RNA-Seq', 'WGS', 'RNA-Seq', 'WXS', 'RNA-Seq', 'WGS'],
                'library_source_material': ['Bulk Tissue', 'Bulk Tissue', 'Bulk Cells', 'Bulk Tissue', 'Single-cells', 'Bulk Tissue'],
                'preservation_method': ['Fresh', 'FFPE', 'Fresh', 'Frozen', 'Fresh', 'FFPE'],
                'diagnosis': ['Acute Lymphoblastic Leukemia', 'Glioblastoma Multiforme', 'Acute Myeloid Leukemia', 'Acute Lymphoblastic Leukemia', 'Glioblastoma', 'Acute Myeloid Leukemia'],
                'age_at_diagnosis': ['2555', '4015', '3285', '2555', '4015', '3285'],
                'age_at_collection': ['2600', '4380', '3650', '2700', '4200', '3500']
            }
            pd.DataFrame(samples_data).to_csv(samples_file, index=False)
            logger.info(f"Created sample samples data: {samples_file}")
        
        # Create sample files data
        files_file = self.data_dir / "files.csv"
        if not files_file.exists():
            files_data = {
                'namespace_organization': ['STJUDE', 'TREEHOUSE', 'COG', 'STJUDE', 'TREEHOUSE'],
                'namespace_name': ['PNOC', 'COMPBIO', 'AML0531', 'PNOC', 'COMPBIO'],
                'file_name': ['RNASeq_001.fastq.gz', 'WGS_002.bam', 'RNASeq_003.fastq.gz', 'WXS_004.bam', 'scRNA_005.h5'],
                'sample_namespace_organization': ['STJUDE', 'TREEHOUSE', 'COG', 'STJUDE', 'TREEHOUSE'],
                'sample_namespace_name': ['PNOC', 'COMPBIO', 'AML0531', 'PNOC', 'COMPBIO'],
                'sample_names': ['SAMPLE001', 'SAMPLE002', 'SAMPLE003', 'SAMPLE004', 'SAMPLE005'],
                'type': ['FASTQ', 'BAM', 'FASTQ', 'BAM', 'HDF5'],
                'size': ['1073741824', '2147483648', '536870912', '3221225472', '268435456'],
                'md5_checksum': ['d41d8cd98f00b204e9800998ecf8427e', 'e3b0c44298fc1c149afbf4c8996fb924', 'da39a3ee5e6b4b0d3255bfef95601890', '5d41402abc4b2a76b9719d911017c592', '7d793037a0760186574b0282f2f435e7'],
                'description': ['RNA sequencing raw reads', 'Whole genome sequencing aligned reads', 'RNA sequencing raw reads', 'Whole exome sequencing aligned reads', 'Single cell RNA sequencing count matrix']
            }
            pd.DataFrame(files_data).to_csv(files_file, index=False)
            logger.info(f"Created sample files data: {files_file}")
        
        # Create sample namespaces data  
        namespaces_file = self.data_dir / "namespaces.csv"
        if not namespaces_file.exists():
            namespaces_data = {
                'organization': ['STJUDE', 'TREEHOUSE', 'COG'],
                'name': ['PNOC', 'COMPBIO', 'AML0531'],
                'description': ['Pediatric Neuro-Oncology Consortium', 'Computational Biology Initiative', 'Acute Myeloid Leukemia Study'],
                'contact_email': ['pnoc@stjude.org', 'compbio@treehouse.org', 'aml@cog.org'],
                'study_short_title': ['PNOC Study', 'Treehouse Study', 'COG AML Study'],
                'study_name': ['Pediatric Neuro-Oncology Consortium Study', 'Treehouse Computational Biology Study', 'Children\'s Oncology Group AML Study'],
                'study_id': ['PNOC001', 'TREE001', 'AAML0531']
            }
            pd.DataFrame(namespaces_data).to_csv(namespaces_file, index=False)
            logger.info(f"Created sample namespaces data: {namespaces_file}")
        
        # Create sample organizations data
        organizations_file = self.data_dir / "organizations.csv"
        if not organizations_file.exists():
            organizations_data = {
                'identifier': ['STJUDE', 'TREEHOUSE', 'COG'],
                'name': ['St. Jude Children\'s Research Hospital', 'UCSC Treehouse', 'Children\'s Oncology Group'],
                'institution': ['SJCRH', 'UCSC', 'COG']
            }
            pd.DataFrame(organizations_data).to_csv(organizations_file, index=False)
            logger.info(f"Created sample organizations data: {organizations_file}")
    
    async def _load_subjects(self):
        """Load subjects data."""
        try:
            subjects_file = self.data_dir / "subjects.csv"
            self.subjects_df = pd.read_csv(subjects_file,dtype={'subject_name': str})
            self.subjects_df = self.subjects_df.fillna('')  # Replace NaN with empty strings
            logger.info(f"Loaded {len(self.subjects_df)} subjects")
        except Exception as e:
            logger.error(f"Error loading subjects: {e}")
            self.subjects_df = pd.DataFrame()
    
    async def _load_samples(self):
        """Load samples data."""
        try:
            samples_file = self.data_dir / "samples.csv"
            self.samples_df = pd.read_csv(samples_file)
            self.samples_df = self.samples_df.fillna('')  # Replace NaN with empty strings
            logger.info(f"Loaded {len(self.samples_df)} samples")
        except Exception as e:
            logger.error(f"Error loading samples: {e}")
            self.samples_df = pd.DataFrame()
    
    async def _load_files(self):
        """Load files data."""
        try:
            files_file = self.data_dir / "files.csv"
            self.files_df = pd.read_csv(files_file)
            self.files_df = self.files_df.fillna('')  # Replace NaN with empty strings
            logger.info(f"Loaded {len(self.files_df)} files")
        except Exception as e:
            logger.error(f"Error loading files: {e}")
            self.files_df = pd.DataFrame()
    
    async def _load_namespaces(self):
        """Load namespaces data."""
        try:
            namespaces_file = self.data_dir / "namespaces.csv"
            self.namespaces_df = pd.read_csv(namespaces_file)
            self.namespaces_df = self.namespaces_df.fillna('')  # Replace NaN with empty strings
            logger.info(f"Loaded {len(self.namespaces_df)} namespaces")
        except Exception as e:
            logger.error(f"Error loading namespaces: {e}")
            self.namespaces_df = pd.DataFrame()
    
    async def _load_organizations(self):
        """Load organizations data."""
        try:
            organizations_file = self.data_dir / "organizations.csv"
            self.organizations_df = pd.read_csv(organizations_file)
            self.organizations_df = self.organizations_df.fillna('')  # Replace NaN with empty strings
            logger.info(f"Loaded {len(self.organizations_df)} organizations")
        except Exception as e:
            logger.error(f"Error loading organizations: {e}")
            self.organizations_df = pd.DataFrame()
    
    def filter_dataframe(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to a DataFrame."""
        if df.empty:
            return df
            
        filtered_df = df.copy()
        
        for field, value in filters.items():
            if value is not None and value != '':
                # Handle exact match filtering
                if field in filtered_df.columns:
                    # For string fields, do case-sensitive exact match
                    mask = filtered_df[field].astype(str) == str(value)
                    filtered_df = filtered_df[mask]
                else:
                    # Handle unharmonized fields (metadata.unharmonized.<field>)
                    if field.startswith('metadata.unharmonized.'):
                        # For now, skip unharmonized field filtering
                        continue
        
        return filtered_df
    
    def paginate_dataframe(self, df: pd.DataFrame, page: int, per_page: int) -> pd.DataFrame:
        """Apply pagination to a DataFrame."""
        if df.empty:
            return df
            
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        return df.iloc[start_idx:end_idx]
    
    def count_by_field(self, df: pd.DataFrame, field: str) -> List[Dict[str, Any]]:
        """Group by field and return counts."""
        if df.empty or field not in df.columns:
            return []
        
        counts = df[field].value_counts()
        return [{"name": str(name), "count": int(count)} for name, count in counts.items()]
    
    @lru_cache(maxsize=128)
    def get_subject_by_id(self, organization: str, namespace: str, name: str) -> Optional[Dict[str, Any]]:
        """Get a subject by its identifier."""
        if self.subjects_df is None or self.subjects_df.empty:
            return None
            
        mask = (
            (self.subjects_df['namespace_organization'] == organization) &
            (self.subjects_df['namespace_name'] == namespace) &
            (self.subjects_df['subject_name'] == name)
        )
        
        matches = self.subjects_df[mask]
        if matches.empty:
            return None
            
        return matches.iloc[0].to_dict()
    
    @lru_cache(maxsize=128)
    def get_sample_by_id(self, organization: str, namespace: str, name: str) -> Optional[Dict[str, Any]]:
        """Get a sample by its identifier."""
        if self.samples_df is None or self.samples_df.empty:
            return None
            
        mask = (
            (self.samples_df['namespace_organization'] == organization) &
            (self.samples_df['namespace_name'] == namespace) &
            (self.samples_df['sample_name'] == name)
        )
        
        matches = self.samples_df[mask]
        if matches.empty:
            return None
            
        return matches.iloc[0].to_dict()
    
    @lru_cache(maxsize=128)
    def get_file_by_id(self, organization: str, namespace: str, name: str) -> Optional[Dict[str, Any]]:
        """Get a file by its identifier."""
        if self.files_df is None or self.files_df.empty:
            return None
            
        mask = (
            (self.files_df['namespace_organization'] == organization) &
            (self.files_df['namespace_name'] == namespace) &
            (self.files_df['file_name'] == name)
        )
        
        matches = self.files_df[mask]
        if matches.empty:
            return None
            
        return matches.iloc[0].to_dict()
    
    @lru_cache(maxsize=128)
    def get_namespace_by_id(self, organization: str, namespace: str) -> Optional[Dict[str, Any]]:
        """Get a namespace by its identifier."""
        if self.namespaces_df is None or self.namespaces_df.empty:
            return None
            
        mask = (
            (self.namespaces_df['organization'] == organization) &
            (self.namespaces_df['name'] == namespace)
        )
        
        matches = self.namespaces_df[mask]
        if matches.empty:
            return None
            
        return matches.iloc[0].to_dict()
    
    @lru_cache(maxsize=128)
    def get_organization_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get an organization by name."""
        if self.organizations_df is None or self.organizations_df.empty:
            return None
            
        mask = self.organizations_df['identifier'] == name
        matches = self.organizations_df[mask]
        if matches.empty:
            return None
            
        return matches.iloc[0].to_dict()
