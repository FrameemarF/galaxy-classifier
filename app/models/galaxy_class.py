from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.models.prediction import PredictionDB


class GalaxyClassDB(Base):
    __tablename__ = "galaxy_classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    model_index: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    description: Mapped[str]

    predictions: Mapped[list["PredictionDB"]] = relationship(back_populates="galaxy_class")