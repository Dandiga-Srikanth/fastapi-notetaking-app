from sqlalchemy_continuum import make_versioned
make_versioned(user_cls=None)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.environment_variables import EnvironmentVariables

SQLALCHEMY_DATABASE_URL = EnvironmentVariables.POSTGRESQL_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()