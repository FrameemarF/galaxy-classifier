from datetime import datetime, timedelta, timezone

import argon2
import jwt

from app.core.config import settings

hasher = argon2.PasswordHasher()

def hash_password(password: str) -> str:
    """
    Хэширует пароль
    """
    return hasher.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """
    Проверяет, совпадает ли хэш
    """
    try:
        hasher.verify(hash=hashed, password=password)
    except argon2.exceptions.VerifyMismatchError:
        return False
    return True

def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        decoded = jwt.decode(jwt=token, algorithms=[settings.ALGORITHM], key=settings.SECRET_KEY)
    except jwt.InvalidTokenError:
        return None
    return int(decoded["sub"])