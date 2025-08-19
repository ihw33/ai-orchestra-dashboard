"""
Global error handling middleware and exception mappers
Issue #15: 에러 핸들링 미들웨어
"""

from typing import Any, Dict
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
import uuid
import traceback


class AppError(Exception):
    def __init__(self, message: str, *, status_code: int = 400, code: str = "app_error", details: Dict[str, Any] | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.details = details or {}


def _error_body(message: str, *, code: str, request_id: str, details: Dict[str, Any] | None = None):
    return {
        "ok": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
        },
        "request_id": request_id,
    }


def register_exception_handlers(app: FastAPI) -> None:
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request.state.request_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        return response

    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError):
        rid = getattr(request.state, "request_id", str(uuid.uuid4()))
        return JSONResponse(status_code=exc.status_code, content=_error_body(str(exc), code=exc.code, request_id=rid, details=exc.details))

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        rid = getattr(request.state, "request_id", str(uuid.uuid4()))
        return JSONResponse(status_code=exc.status_code, content=_error_body(exc.detail or "HTTP error", code="http_error", request_id=rid))

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        rid = getattr(request.state, "request_id", str(uuid.uuid4()))
        return JSONResponse(status_code=422, content=_error_body("Validation error", code="validation_error", request_id=rid, details={"errors": exc.errors()}))

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception):
        rid = getattr(request.state, "request_id", str(uuid.uuid4()))
        # NOTE: For development, include traceback in details. Strip in production if needed.
        return JSONResponse(status_code=500, content=_error_body("Internal server error", code="internal_error", request_id=rid, details={"trace": traceback.format_exc()}))

