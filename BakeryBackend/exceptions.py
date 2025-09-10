"""
Custom Exception Classes for Bakery Backend
"""

from fastapi import HTTPException
from typing import Optional, Any, Dict


class BakeryBaseException(Exception):
    """Base exception class for all bakery-related exceptions"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class DatabaseError(BakeryBaseException):
    """Raised when database operations fail"""
    
    def __init__(self, message: str = "Database operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class ValidationError(BakeryBaseException):
    """Raised when data validation fails"""
    
    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class UnauthorizedError(BakeryBaseException):
    """Raised when user is not authorized"""
    
    def __init__(self, message: str = "Unauthorized access", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class NotFoundError(BakeryBaseException):
    """Raised when requested resource is not found"""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class ConflictError(BakeryBaseException):
    """Raised when there's a conflict in data"""
    
    def __init__(self, message: str = "Data conflict occurred", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)


class BusinessLogicError(BakeryBaseException):
    """Raised when business logic rules are violated"""
    
    def __init__(self, message: str = "Business logic error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)