from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.models.user import UserDB
from app.database.database import get_session, Session
from app.database.crud import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """
    Получает access token, декодирует и достаёт из базы запись о пользователе
    Если токен некорректный или истёк или пользователь не был найден выдаёт ошибку 401
    """
    decoded_token = decode_access_token(token)

    if decoded_token is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    user = get_user_by_id(session=session, user_id=decoded_token)

    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return user


oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)
def get_optional_user(token: str|None = Depends(oauth2_scheme_optional), session: Session = Depends(get_session)) -> UserDB | None:

    if token is None:
        return None
    
    decoded_token = decode_access_token(token)
    if decoded_token is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    user = get_user_by_id(session=session, user_id=decoded_token)

    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return user