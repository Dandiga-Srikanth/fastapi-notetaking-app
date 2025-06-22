from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.dependencies.db import get_db
from app.crud import user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(email: str, db:Session = Depends(get_db)):
    return user.get_user_by_email(db, email)


def authenticate_user(db:Session, email: str, password: str):
    user = get_user(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user does not exist"
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user