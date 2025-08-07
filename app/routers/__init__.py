"""
Router modules for CCDI API.
"""

# Import all routers to make them available
from . import subject
from . import sample
from . import file
from . import metadata
from . import namespace
from . import organization
from . import info

__all__ = [
    "subject",
    "sample", 
    "file",
    "metadata",
    "namespace",
    "organization",
    "info"
]
