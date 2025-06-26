from sqlalchemy.orm import Session
from app.models.role import Role

def has_permission(db: Session, role_id: int, permission_name: str) -> bool:
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        return False
    return any(p.name == permission_name for p in role.permissions)