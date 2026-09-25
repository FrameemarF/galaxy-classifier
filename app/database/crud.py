from sqlalchemy.orm import Session
from app.models.galaxy_class import GalaxyClassDB
from app.models.prediction import PredictionDB
from sqlalchemy import select

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