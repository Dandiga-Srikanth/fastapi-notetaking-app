from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from app.auth.jwt import verify_token_access
from app.dependencies.db import get_db
from app.models.user import User
from app.crud.user import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

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
