from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Categories(str, Enum):
    FIRE = "Пожар"
    CRIME = "Преступление"
    DTP = "ДТП"


class PostWriteModel(BaseModel):
    title: str
    incident_id: int | None = Field(
        default=None
    )


class IncidentWriteModel(BaseModel):
    longitude: float
    latitude: float
    category: Categories


class PostReadModel(BaseModel):
    user_id: int
    title: str
    media_path: str | None = Field(
        default=None
    )
    created_at: datetime

    class Config:
        orm_mode = True


class IncidentReadModel(BaseModel):
    id: int
    longitude: float
    latitude: float
    address: str
    is_predictive: bool
    is_active: bool
    category: str
    created_at: datetime

    class Config:
        orm_mode = True
