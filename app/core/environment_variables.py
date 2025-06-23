import os
from dotenv import load_dotenv
load_dotenv()

class EnvironmentVariables:
    POSTGRESQL_DATABASE_URL = os.getenv("POSTGRESQL_DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    POSTGRESQL_TEST_DATABASE_URL = os.getenv("POSTGRESQL_TEST_DATABASE_URL")
    TEST_USER_ACCOUNT_PASSWORD = os.getenv("TEST_USER_ACCOUNT_PASSWORD")