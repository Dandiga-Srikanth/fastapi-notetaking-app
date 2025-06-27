from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate
from app.auth.security import hash_password
from sqlalchemy import func
from app.exceptions.handlers import DuplicateUserException


def get_user_by_id(db: Session, user_id: int, status:str = "active") -> User | None:
    if status == 'active':
        return db.query(User).filter(User.id == user_id, User.is_active==True).first()
    elif status=='inactive':
        return db.query(User).filter(User.id == user_id, User.is_active==False).first()
    else:
        return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str, status:str = "active") -> User | None:
    if status == 'active':
        return db.query(User).filter(func.lower(User.email)==email.lower(), User.is_active==True).first()
    elif status == 'inactive':
        return db.query(User).filter(func.lower(User.email)==email.lower(), User.is_active==False).first()
    else:
        return db.query(User).filter(func.lower(User.email)==email.lower()).first()

def get_all_users(db: Session, status: str="active") -> list[User]:
    if status == 'active':
        return db.query(User).filter(User.is_active==True).all()
    elif status == 'inactive':
        return db.query(User).filter(User.is_active==False).all()
    else:
        return db.query(User).all()

def create_user(db: Session, user_in: UserCreate) -> User:
    role_id = None
    if user_in.role_name:
        role = db.query(Role).filter(Role.name == user_in.role_name.value).first()
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role name")
        role_id = role.id

    db_user = User(
        email=user_in.email,
        password=hash_password(user_in.password),
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        role_id=role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_in: UserUpdate) -> User | None:
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    existing_user = get_user_by_email(db, email=user_in.email, status="all")
    if existing_user:
        raise DuplicateUserException
    
    for field, value in user_in.dict(exclude_unset=True).items():
        if field == "password":
            value = hash_password(value)
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    user.is_active = False
    db.commit()
    db.refresh(user)
    return True
