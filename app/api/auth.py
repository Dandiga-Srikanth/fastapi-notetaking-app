from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.auth.security import authenticate_user
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/api/v1/auth/login", tags=["Authentication"])

from app.schemas.auth import Token

@router.post("/", response_model=Token)
async def login_for_access_token(
    user_details: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:Session = Depends(get_db)

) -> Token:
    user = authenticate_user(db, user_details.username, user_details.password)
    access_token = create_access_token(
        data={"sub": user.email, "user_id":user.id, "role":user.role_id}
    )
    return Token(access_token=access_token, token_type="bearer")