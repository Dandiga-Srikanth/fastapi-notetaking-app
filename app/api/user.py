from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Annotated

from app import schemas, crud
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_active_user
from app.exceptions.handlers import DuplicateUserException
from app.models.user import User


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post("/", response_model=schemas.user.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.user.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.user.get_user_by_email(db, user_in.email, status="all")
    if existing_user:
        raise DuplicateUserException
    return crud.user.create_user(db, user_in)


@router.get("/", response_model=List[schemas.user.UserRead])
def list_users(db: Session = Depends(get_db)):
    return crud.user.get_all_users(db)


@router.get("/{user_id}", response_model=schemas.user.UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=schemas.user.UserRead)
def update_user(user_id: int, user_in: schemas.user.UserUpdate, db: Session = Depends(get_db)):
    user = crud.user.update_user(db, user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    print("user_id",user_id)
    success = crud.user.delete_user(db, int(user_id))
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return
