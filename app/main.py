"""
CCDI Data Federation API

FastAPI implementation of the CCDI Data Federation Participating Nodes API.
This API provides access to subjects, samples, files, and metadata.
"""

from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from app.routers import subject, sample, file, metadata, namespace, organization, info
from app.services.data_loader import DataLoader


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting CCDI API server...")
    
    # Load data on startup
    data_loader = DataLoader()
    await data_loader.load_all_data()
    app.state.data_loader = data_loader
    
    logger.info("CCDI API server started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down CCDI API server...")


# Create FastAPI app
app = FastAPI(
    title="CCDI Data Federation: Participating Nodes API",
    description="""
    This is the concrete OpenAPI specification for the CCDI
    Data Federation API—though this document contains all of the API calls
    that CCDI Federation nodes must implement, it does not outline the
    complete specification.

    * Visit the [documentation homepage](https://cbiit.github.io/ccdi-federation-api)
      to view the complete set of requirements to maintain and deploy a CCDI
      Federation node.
    * Additionally, you can view the Swagger specification in a more traditional
      theme by visiting
      [this link](https://cbiit.github.io/ccdi-federation-api/specification.html).
    * To access CCDI Data Federation Resource, please visit
      [this link](https://cbiit.github.io/ccdi-federation-api-aggregation/).
    """,
    version="v1.2.0",
    contact={
        "name": "Childhood Cancer Data Initiative support email",
        "email": "NCIChildhoodCancerDataInitiative@mail.nih.gov"
    },
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API router with v1 prefix
api_v1_router = APIRouter(prefix="/api/v1")

# Include all routers under the API v1 router
api_v1_router.include_router(subject.router, prefix="/subject", tags=["Subject"])
api_v1_router.include_router(sample.router, prefix="/sample", tags=["Sample"])
api_v1_router.include_router(file.router, prefix="/file", tags=["File"])
api_v1_router.include_router(metadata.router, prefix="/metadata", tags=["Metadata"])
api_v1_router.include_router(namespace.router, prefix="/namespace", tags=["Namespace"])
api_v1_router.include_router(organization.router, prefix="/organization", tags=["Organization"])
api_v1_router.include_router(info.router, prefix="/info", tags=["Info"])

# Include the API router in the main app
app.include_router(api_v1_router)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "title": "CCDI Data Federation: Participating Nodes API",
        "version": "v1.2.0",
        "description": "API for accessing CCDI federated data",
        "endpoints": {
            "subjects": "/api/v1/subject",
            "samples": "/api/v1/sample",
            "files": "/api/v1/file",
            "metadata": "/api/v1/metadata",
            "namespaces": "/api/v1/namespace",
            "organizations": "/api/v1/organization",
            "info": "/api/v1/info",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "errors": [{
                "kind": "NotFound",
                "entity": f"Resource at {request.url.path}",
                "message": f"Resource at {request.url.path} not found."
            }]
        }
    )


@app.exception_handler(422)
async def validation_exception_handler(request: Request, exc):
    """Custom 422 handler for validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "errors": [{
                "kind": "ValidationError",
                "message": "Invalid query or path parameters."
            }]
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
