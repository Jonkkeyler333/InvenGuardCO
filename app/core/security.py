from argon2 import PasswordHasher
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except:
        return False
    
def create_access_token(sub: dict) -> str:
    expire = datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub" : sub,
        "exp" : expire
    }
    token = jwt.encode(payload, key = SECRET_KEY, algorithm = ALGORITHM)
    return token

def verify_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise ValueError("Invalid token")
    sub : str | None = payload.get("sub")
    if sub is None:
        raise ValueError("Invalid token")
    if datetime.now(timezone.utc) > datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc):
        raise ValueError("Invalid token")
    return sub
    