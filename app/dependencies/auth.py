from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from app.auth.jwt import verify_token_access
from app.dependencies.db import get_db
from app.models.user import User
from app.crud.user import get_user_by_id
from jose import jwt, JWTError
from app.core.environment_variables import EnvironmentVariables
from app.core.config import ALGORITHM
from app.auth.permissions import has_permission


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not Validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    try:
        token = verify_token_access(token, credentials_exception)
        user = get_user_by_id(db,token.user_id)
        if user is None:
            raise credentials_exception
    except:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):

    if not current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


def RBACPermission(required_permission: str):
    async def dependency(request: Request, db=Depends(get_db)):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, EnvironmentVariables.SECRET_KEY, algorithms=[ALGORITHM])

            role_id = payload.get("role_id")
            if not role_id:
                raise HTTPException(status_code=403, detail="Missing role_id in token")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        if not has_permission(db, role_id, required_permission):
            raise HTTPException(status_code=403, detail="Access denied")

    return dependency
