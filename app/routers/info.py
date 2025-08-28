"""
Info router for CCDI API.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
import logging
from datetime import datetime, timezone

from app.models import InfoResponse, ServerInfo, APIInfo, VersionInfo, DataInfo
from app.services.data_loader import DataLoader

logger = logging.getLogger(__name__)
router = APIRouter()


def get_data_loader(request: Request) -> DataLoader:
    """Dependency to get the data loader from app state."""
    return request.app.state.data_loader


@router.get("", response_model=InfoResponse)
async def get_info(data_loader: DataLoader = Depends(get_data_loader)):
    """Get information about this server."""
    try:
        server_info = ServerInfo(
            name="IUSCCC CCDI Data Federation API Server",
            version="v1.2.0",
            owner="Indiana University Simon Comprehensive Cancer Center",
            contact_email="su1@iu.edu",
            description="FastAPI implementation of the CCDI Data Federation Participating Nodes API",
        )

        api_info = APIInfo(
            api_version="v1.2.0",
            documentation_url="https://cbiit.github.io/ccdi-federation-api/specification.html",
        )

        version_info = VersionInfo(version="1", about="")

        data_info = DataInfo(
            version=version_info,
            last_updated=datetime.now(timezone.utc).isoformat(),
            source="Indiana University Simon Comprehensive Cancer Center",
            wiki_url="https://github.com/CBIIT/ccdi-federation-api-spec/wiki",
        )

        return InfoResponse(server=server_info, api=api_info, data=data_info)

    except Exception as e:
        logger.error(f"Error getting server info: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
