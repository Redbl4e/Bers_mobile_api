from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from fastapi_users_db_sqlalchemy.generics import TIMESTAMPAware, now_utc
from sqlalchemy import Integer, String, Boolean, func, Column, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

AuthBase = declarative_base()


class User(SQLAlchemyBaseUserTable[int], AuthBase):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(length=50), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    created_at: datetime = Column(
        DateTime, server_default=func.now()
    )
    updated_at: datetime = Column(
        DateTime, onupdate=func.now()
    )


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], AuthBase):
    token: Mapped[str] = mapped_column(String(length=43), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPAware(timezone=True), index=True, nullable=False, default=now_utc
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id, ondelete="cascade"), nullable=False
    )
