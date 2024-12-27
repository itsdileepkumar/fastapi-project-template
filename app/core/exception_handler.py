from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pymongo.errors import PyMongoError
from pydantic import ValidationError


async def unified_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    client_errors: tuple = (
        ArithmeticError,
        AssertionError,
        AttributeError,
        EOFError,
        LookupError,
        NameError,
        StopIteration,
        StopAsyncIteration,
        SyntaxError,
        TypeError,
        ValueError,
        Warning,
    )
    server_errors: tuple = (
        BufferError,
        ImportError,
        MemoryError,
        OSError,
        ReferenceError,
        RuntimeError,
        SystemError,
        PyMongoError,
    )
    validation_errors: tuple = (ValidationError, RequestValidationError)
    http_errors: tuple = (HTTPException, StarletteHTTPException)

    if isinstance(exc, http_errors):
        status_code = exc.status_code
        detail = exc.detail or str(exc)
        content = {"message": f"{exc.__class__.__name__}", "detail": detail}
    elif isinstance(exc, validation_errors):
        status_code = 422
        detail = exc.errors().__str__() or str(exc)
        content = {"message": f"{exc.__class__.__name__}", "detail": detail}
    elif isinstance(exc, client_errors):
        status_code = 400
        content = {"message": f"{exc.__class__.__name__}", "detail": str(exc)}
    elif isinstance(exc, server_errors):
        status_code = 500
        content = {"message": f"{exc.__class__.__name__}", "detail": str(exc)}
    else:
        status_code = 500
        content = {"message": "Internal Server Error", "detail": str(exc)}

    return JSONResponse(status_code=status_code, content=content)
