import jwt
from fastapi import Request, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import RequestResponseEndpoint
from app.config import settings


# async def auth_middleware(
#     request: Request, call_next: RequestResponseEndpoint
# ) -> StreamingResponse:
#     try:
#         token: str = request.headers.get(settings.IDENTITY_CONTEXT_HEADER, None)
#         if not token:
#             raise HTTPException(status_code=401, detail="No token provided")
#         payload: dict = jwt.decode(token, options={"verify_signature": False})
#         request.state.authInfo = payload
#         response: Response = await call_next(request)
#         return response
#     except Exception as e:
#         if isinstance(e, HTTPException):
#             print(e)
#             return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
#         if isinstance(e, jwt.PyJWTError):
#             print(e)
#             return JSONResponse(status_code=401, content={"detail": "Invalid token"})
#         print(e)
#         return JSONResponse(
#             status_code=500, content={"detail": "Internal server error"}
#         )


async def auth_middleware(request: Request) -> None:
    try:
        token: str = request.headers.get(settings.IDENTITY_CONTEXT_HEADER, None)
        if not token:
            raise HTTPException(status_code=401, detail="No token provided")
        payload: dict = jwt.decode(token, options={"verify_signature": False})
        for key, value in payload.items():
            setattr(request.state, key, value)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        if isinstance(e, jwt.PyJWTError):
            raise HTTPException(status_code=401, detail=f"Invalid token - {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error - {e}")
