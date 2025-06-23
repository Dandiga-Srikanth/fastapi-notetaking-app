from sqlalchemy.orm import Session

def has_permission(db: Session, role_id: int, permission_name: str) -> bool:
    result = db.execute(
        """
        SELECT 1
        FROM role_permissions rp
        JOIN permissions p ON p.id = rp.permission_id
        WHERE rp.role_id = :role_id AND p.name = :perm
        LIMIT 1
        """,
        {"role_id": role_id, "perm": permission_name},
    )
    return result.scalar() is not None