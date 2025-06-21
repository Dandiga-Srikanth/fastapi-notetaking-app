import os
from dotenv import load_dotenv
load_dotenv()

class EnvironmentVariables:
    POSTGRESQL_DATABASE_URL = os.getenv("POSTGRESQL_DATABASE_URL")