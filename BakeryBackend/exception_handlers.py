"""
Global Exception Handlers for Bakery Backend
"""

import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError as PydanticValidationError

from .exceptions import (
    BakeryBaseException,
    DatabaseError,
    ValidationError,
    UnauthorizedError,
    NotFoundError,
    ConflictError,
    BusinessLogicError
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_error_response(
    status_code: int,
    error_type: str,
    message: str,
    details: Dict[str, Any] = None,
    request_id: str = None
) -> JSONResponse:
    """
    Create a standardized error response
    """
    error_response = {
        "error": {
            "type": error_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "status_code": status_code
        }
    }
    
    if details:
        error_response["error"]["details"] = details
        
    if request_id:
        error_response["error"]["request_id"] = request_id
    
    return JSONResponse(
        status_code=status_code,
        content=error_response
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle FastAPI HTTPException"""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return create_error_response(
        status_code=exc.status_code,
        error_type="HTTPException",
        message=str(exc.detail),
        request_id=getattr(request.state, 'request_id', None)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle FastAPI validation errors"""
    logger.warning(f"Validation Error: {exc.errors()}")
    
    # Format validation errors for better readability
    formatted_errors = []
    for error in exc.errors():
        formatted_errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return create_error_response(
        status_code=422,
        error_type="ValidationError",
        message="Request validation failed",
        details={"validation_errors": formatted_errors},
        request_id=getattr(request.state, 'request_id', None)
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle SQLAlchemy database errors"""
    logger.error(f"Database Error: {str(exc)}")
    
    error_message = "Database operation failed"
    status_code = 500
    
    # Handle specific database errors
    if isinstance(exc, IntegrityError):
        error_message = "Data integrity constraint violation"
        status_code = 409
    
    return create_error_response(
        status_code=status_code,
        error_type="DatabaseError",
        message=error_message,
        details={"error_details": str(exc) if logger.level <= logging.DEBUG else None},
        request_id=getattr(request.state, 'request_id', None)
    )


async def custom_database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """Handle custom DatabaseError"""
    logger.error(f"Custom Database Error: {exc.message}")
    
    return create_error_response(
        status_code=500,
        error_type="DatabaseError",
        message=exc.message,
        details=exc.details,
        request_id=getattr(request.state, 'request_id', None)
    )


async def custom_validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle custom ValidationError"""
    logger.warning(f"Custom Validation Error: {exc.message}")
    
    return create_error_response(
        status_code=400,
        error_type="ValidationError",
        message=exc.message,
        details=exc.details,
        request_id=getattr(request.state, 'request_id', None)
    )


async def unauthorized_error_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    """Handle UnauthorizedError"""
    logger.warning(f"Unauthorized Error: {exc.message}")
    
    return create_error_response(
        status_code=401,
        error_type="UnauthorizedError",
        message=exc.message,
        details=exc.details,
        request_id=getattr(request.state, 'request_id', None)
    )


async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    """Handle NotFoundError"""
    logger.info(f"Not Found Error: {exc.message}")
    
    return create_error_response(
        status_code=404,
        error_type="NotFoundError",
        message=exc.message,
        details=exc.details,
        request_id=getattr(request.state, 'request_id', None)
    )


async def conflict_error_handler(request: Request, exc: ConflictError) -> JSONResponse:
    """Handle ConflictError"""
    logger.warning(f"Conflict Error: {exc.message}")
    
    return create_error_response(
        status_code=409,
        error_type="ConflictError",
        message=exc.message,
        details=exc.details,
        request_id=getattr(request.state, 'request_id', None)
    )


async def business_logic_error_handler(request: Request, exc: BusinessLogicError) -> JSONResponse:
    """Handle BusinessLogicError"""
    logger.warning(f"Business Logic Error: {exc.message}")
    
    return create_error_response(
        status_code=400,
        error_type="BusinessLogicError",
        message=exc.message,
        details=exc.details,
        request_id=getattr(request.state, 'request_id', None)
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions"""
    logger.error(f"Unhandled Exception: {str(exc)}", exc_info=True)
    
    return create_error_response(
        status_code=500,
        error_type="InternalServerError",
        message="An unexpected error occurred",
        details={"error_details": str(exc) if logger.level <= logging.DEBUG else None},
        request_id=getattr(request.state, 'request_id', None)
    )


async def pydantic_validation_error_handler(request: Request, exc: PydanticValidationError) -> JSONResponse:
    """Handle Pydantic validation errors"""
    logger.warning(f"Pydantic Validation Error: {exc.errors()}")
    
    formatted_errors = []
    for error in exc.errors():
        formatted_errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return create_error_response(
        status_code=422,
        error_type="ValidationError",
        message="Data validation failed",
        details={"validation_errors": formatted_errors},
        request_id=getattr(request.state, 'request_id', None)
    )