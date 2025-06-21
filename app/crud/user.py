from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate
from app.auth.security import hash_password


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    role_id = None
    if user_in.role_name:
        role = db.query(Role).filter(Role.name == user_in.role_name.value).first()
        if not role:
            raise HTTPException(status_code=400, detail="Invalid role name")
        role_id = role.id
    print("role_id", role_id)

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
    db.delete(user)
    db.commit()
    return True
