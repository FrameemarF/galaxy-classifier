from app.models.galaxy_class import GalaxyClassDB
from app.models.prediction import PredictionDB
from app.models.user import UserDB
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

def take_galaxy_entry(session: Session, model_index: int) -> GalaxyClassDB:
    """
    Функция для получения id типа галактики по индексу от модели
    """
    query = select(GalaxyClassDB).where(GalaxyClassDB.model_index == model_index)
    result = session.scalar(query)
    return result

def create_prediction_entry(session: Session, galaxy_id: int, confidence: float, image_path: str, user_id: int = None):
    """
    Функция для создания записи предсказания в БД
    """
    new_prediction = PredictionDB(galaxy_class_id=galaxy_id, confidence=confidence, image_path=image_path, user_id=user_id)
    session.add(new_prediction)
    session.commit()

def get_user_by_email(session: Session, email) -> UserDB | None:
    """
    Получить запись о пользователе по его email
    """
    query = select(UserDB).where(UserDB.email == email)
    return session.scalar(query)

def get_user_by_id(session: Session, user_id) -> UserDB | None:
    """
    Получить запись о пользователе по его id в БД
    """
    return session.get(UserDB, user_id)

def create_user(session: Session, email: str, hashed_password) -> UserDB:
    """
    Создать пользователя в БД
    """
    new_user = UserDB(email=email.lower(), hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

def get_predictions_by_user(session: Session, user_id: int, limit: int = 20, offset: int = 0) -> list[PredictionDB]:
    """
    Получить историю предсказаний пользователя
    """
    query = select(PredictionDB).where(PredictionDB.user_id == user_id).order_by(PredictionDB.created_at.desc(), PredictionDB.id.desc()).options(selectinload(PredictionDB.galaxy_class)).limit(limit).offset(offset)
    return list(session.scalars(query).all())