"""
Middleware for Bakery Backend
"""

import uuid
import time
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

logger = logging.getLogger(__name__)


class RequestMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add request ID and log requests
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Add request ID to response headers
        start_time = time.time()
        
        # Log incoming request
        logger.info(
            f"Request started - ID: {request_id} | "
            f"Method: {request.method} | "
            f"URL: {request.url} | "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            response = await call_next(request)
            
            # Calculate request duration
            duration = time.time() - start_time
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            # Log response
            logger.info(
                f"Request completed - ID: {request_id} | "
                f"Status: {response.status_code} | "
                f"Duration: {duration:.3f}s"
            )
            
            return response
            
        except Exception as exc:
            duration = time.time() - start_time
            logger.error(
                f"Request failed - ID: {request_id} | "
                f"Duration: {duration:.3f}s | "
                f"Error: {str(exc)}"
            )
            raise exc