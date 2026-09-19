from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import func, DateTime, ForeignKey
from app.database.database import Base
from datetime import datetime


class PredictionDB(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
        )
    galaxy_class_id: Mapped[int] = mapped_column(ForeignKey("galaxy_classes.id"))
    confidence: Mapped[float]
    image_path: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    user: Mapped["UserDB"] = relationship(back_populates="predictions")
    galaxy_class: Mapped["GalaxyClassDB"] = relationship(back_populates="predictions")