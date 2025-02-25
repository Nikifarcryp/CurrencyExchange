import datetime

from sqlalchemy import BigInteger, DateTime, func, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    registered_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
