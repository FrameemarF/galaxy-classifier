from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.database.crud import create_user, get_user_by_email
from app.database.database import get_session
from app.models import UserDB
from app.schemas.user import Register, Token, User

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/registration", response_model=User, status_code=201)
def register_new_user(reg_info: Register, session: Session = Depends(get_session)):
    email = reg_info.email.lower()
    user = get_user_by_email(session=session, email=email)

    if user is not None:
        raise HTTPException(status_code=409, detail="User already exist")
    
    hashed_password = hash_password(reg_info.password)

    try:
        user = create_user(session=session, email=email, hashed_password=hashed_password)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="User already exist")
    return user

@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):

    user = get_user_by_email(session=session, email=form.username.lower())

    if user is None or not(verify_password(form.password, hashed=user.hashed_password)):
        raise HTTPException(headers={"WWW-Authenticate": "Bearer"}, status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(user_id=user.id)

    return {"access_token": access_token}

@router.get("/me", response_model=User)
def me(current_user: UserDB = Depends(get_current_user)):
    return current_user