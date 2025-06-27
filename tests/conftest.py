import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from alembic.config import Config
from alembic import command

from app.dependencies.db import get_db
from app.main import app
from app.core.environment_variables import EnvironmentVariables
from app.models.role import Role
from app.models.permission import Permission

# Use a separate test database
TEST_DATABASE_URL = EnvironmentVariables.POSTGRESQL_TEST_DATABASE_URL

# Override database for test DB
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """
    Apply Alembic migrations once before running tests.
    """
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

@pytest.fixture(scope="function")
def db():
    """
    Start a transaction for each test and roll it back after.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def test_client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def seed_roles_and_permissions(db: Session):

    permission_names = [
        "create_user", "view_user", "update_user", "delete_user",
        "create_note", "view_note", "update_note", "delete_note"
    ]
    permissions = [Permission(name=name) for name in permission_names]
    db.add_all(permissions)
    db.commit()

    permission_map = {perm.name: perm for perm in db.query(Permission).all()}

    role_definitions = {
        "Admin": permission_names,
        "Editor": ["view_user","create_note", "view_note", "update_note"],
        "Viewer": ["view_user", "view_note"],
    }

    for role_name, perm_names in role_definitions.items():
        role = Role(name=role_name)
        role.permissions = [permission_map[name] for name in perm_names]
        db.add(role)

    db.commit()
