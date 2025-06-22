from datetime import timedelta, datetime

from jose import JWTError, jwt

from app.schemas import auth

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from app.core.environment_variables import EnvironmentVariables


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"expire": expire.strftime("%Y-%m-%d %H:%M:%S")})

    encoded_jwt = jwt.encode(to_encode, EnvironmentVariables.SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_token_access(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, EnvironmentVariables.SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = auth.DataToken(user_id=user_id)

    except JWTError as e:
        print(e)
        raise credentials_exception
    
    return token_data