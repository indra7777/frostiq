from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from pydantic import ValidationError as PydanticValidationError

from BakeryBackend.routers import favorites
from BakeryBackend.database import Base, engine
from BakeryBackend.middleware import RequestMiddleware
from BakeryBackend.exceptions import (
    DatabaseError,
    ValidationError,
    UnauthorizedError,
    NotFoundError,
    ConflictError,
    BusinessLogicError
)
from BakeryBackend.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    custom_database_error_handler,
    custom_validation_error_handler,
    unauthorized_error_handler,
    not_found_error_handler,
    conflict_error_handler,
    business_logic_error_handler,
    general_exception_handler,
    pydantic_validation_error_handler
)

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Bakery Backend with Favorites")

# Add middleware
app.add_middleware(RequestMiddleware)

# Register exception handlers
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, database_exception_handler)
app.add_exception_handler(DatabaseError, custom_database_error_handler)
app.add_exception_handler(ValidationError, custom_validation_error_handler)
app.add_exception_handler(UnauthorizedError, unauthorized_error_handler)
app.add_exception_handler(NotFoundError, not_found_error_handler)
app.add_exception_handler(ConflictError, conflict_error_handler)
app.add_exception_handler(BusinessLogicError, business_logic_error_handler)
app.add_exception_handler(PydanticValidationError, pydantic_validation_error_handler)

# Include routers
app.include_router(favorites.router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Bakery Backend API is running!",
        "status": "healthy",
        "features": ["global_exception_handling", "request_logging"]
    }


@app.get("/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-01T00:00:00Z",
        "version": "1.0.0",
        "database": "connected"
    }