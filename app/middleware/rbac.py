from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from jose import jwt, JWTError
from app.db.session import SessionLocal
from app.core.environment_variables import EnvironmentVariables
from app.auth.permissions import has_permission
from app.core.config import ALGORITHM

class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        required_permission = getattr(request.state, "required_permission", None)

        if required_permission:
            token = request.headers.get("Authorization").split(" ")[1]
            try:
                payload = jwt.decode(
                    token,
                    EnvironmentVariables.SECRET_KEY,
                    algorithms=ALGORITHM
                )
                role_id = payload.get("role_id")
                if not role_id:
                    return JSONResponse(status_code=403, content={"detail": "Missing role_id in token"})
            except JWTError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

            db = SessionLocal()
            try:
                if not has_permission(db, role_id, required_permission):
                    return JSONResponse(status_code=403, content={"detail": "Access denied"})
            finally:
                db.close()

        return await call_next(request)
