from datetime import datetime
from pathlib import Path

from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.incident.models import Incident, PostIncident
from src.incident.schemas import Categories


async def save_incident_to_db(
        session: AsyncSession,
        longitude: float,
        latitude: float,
        category: Categories,
        address: str
) -> int:
    incident_insert = insert(Incident).values(
        longitude=longitude,
        latitude=latitude,
        category=category.value,
        address=address,
        created_at=datetime.now()
    ).returning(Incident.id)
    returning = await session.execute(incident_insert)
    incident_id = returning.first()[0]
    return incident_id


async def save_post_to_db(
        session: AsyncSession,
        user: User,
        post_title: str,
        file_path: Path,
        incident_id: int
) -> int:
    post_insert = insert(PostIncident).values(
        user_id=user.id,
        title=post_title,
        media_path=str(file_path),
        incident_id=incident_id,
        created_at=datetime.now()
    ).returning(PostIncident.id)
    print(post_insert)
    returning = await session.execute(post_insert)
    await session.commit()
    post_id = returning.first()[0]
    return post_id


async def change_incident_status(incident_id: int, session: AsyncSession, active: bool):
    query = update(Incident).where(Incident.id == incident_id).values(is_active=active)
    await session.execute(query)
    await session.commit()
