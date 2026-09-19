from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.database.database import Base
from datetime import datetime
import enum

class UserRole(enum.Enum):
    user = "user"
    admin = "admin"

class UserDB(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"),
        default=UserRole.user
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
    predictions: Mapped[list["PredictionDB"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )