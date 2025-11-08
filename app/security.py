from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional

SECRET = 'change-this-secret'
ALGO = 'HS256'
EXP_MIN = 30

def hash_secret(plain: str) -> str:
    return pbkdf2_sha256.hash(plain)

def verify_secret(plain: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(plain, hashed)

def make_token(subject: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=EXP_MIN)
    # use a numeric unix timestamp for 'exp' so JWT libraries validate correctly
    payload = {'sub': subject, 'exp': int(expire.timestamp())}
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def read_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        return payload.get('sub')
    except JWTError:
        return None
