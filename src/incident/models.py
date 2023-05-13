from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, DECIMAL, String, Boolean, TIMESTAMP, func, Column, ForeignKey, Text, DateTime, \
    CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

from auth.models import User

IncidentBase = declarative_base()


class IncidentCategory(Enum):
    FIRE = "Пожар"
    CRIME = "Преступление"
    TRAFFIC_INCIDENT = "ДТП"


class Incident(IncidentBase):
    __tablename__ = "incident"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    longitude: Mapped[float] = mapped_column(
        DECIMAL, nullable=False
    )
    latitude: Mapped[float] = mapped_column(
        DECIMAL, nullable=False
    )
    address: Mapped[str] = mapped_column(
        String
    )
    category: IncidentCategory = Column(
        String, nullable=False
    )
    is_predictive: Mapped[str] = mapped_column(
        Boolean, default=False
    )
    is_active: Mapped[str] = mapped_column(
        Boolean, default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=func.now()
    )
    __table_args__ = (
        CheckConstraint(category.in_(["Пожар", "Преступление", "ДТП"])),
    )


class PostIncident(IncidentBase):
    __tablename__ = "post_incident"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(User.id, ondelete="cascade"), nullable=False
    )
    title: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    media_path: Mapped[str] = mapped_column(
        Text, nullable=True
    )
    incident_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("incident.id", ondelete="cascade"), nullable=False
    )
    created_at: datetime = Column(
        DateTime, server_default=func.now()
    )
