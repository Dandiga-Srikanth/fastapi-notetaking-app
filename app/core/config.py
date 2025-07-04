from enum import Enum

class RoleEnum(str, Enum):
    admin = "Admin"
    editor = "Editor"
    viewer = "Viewer"

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"