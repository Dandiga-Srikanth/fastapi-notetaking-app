from enum import Enum

class RoleEnum(str, Enum):
    admin = "Admin"
    editor = "Editor"
    viewer = "Viewer"