from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from app.settings.base import get_settings


async def api_key_validator(api_key_header: str = Security(APIKeyHeader(name="X-API-Key", auto_error=True))):
    """
    Api key dependency injection

    :param api_key_header:
    :return: None
    """
    if api_key_header != get_settings().API_KEY:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")
