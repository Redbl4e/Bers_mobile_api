from typing import Sequence, Optional, Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, Response, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import FileResponse

from src.auth.config import fastapi_users
from src.auth.models import User
from src.config import MEDIA_PATH, POSTS_PATH
from src.database import get_async_session
from src.incident.models import Incident
from src.incident.schemas import IncidentReadModel, Categories, PostReadModel
from src.incident.services import save_incident_to_db, save_post_to_db, change_incident_status
from src.incident.utils import get_unique_filename, save_file, get_address_from_coords

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"]
)

current_user = fastapi_users.current_user()


@router.post("/add-incident")
async def add_incident(
        longitude: Annotated[float, Form()],
        latitude: Annotated[float, Form()],
        category: Annotated[Categories, Form()],
        post_title: Annotated[str, Form()],
        file: Optional[UploadFile] = File(None),
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> int:
    if file:
        file_path = get_unique_filename(file.filename)
        save_file(file, file_path)
    else:
        file_path = None
    try:
        address = get_address_from_coords(longitude, latitude)
    except Exception as e:
        address = "-"
        print(e)
    incident_id = await save_incident_to_db(session, longitude, latitude, category, address)
    await save_post_to_db(session, user, post_title, file_path, incident_id)

    await session.commit()

    return incident_id


@router.post("/add-post")
async def add_post(
        incident_id: Annotated[int, Form()],
        post_title: Annotated[str, Form()],
        file: Optional[UploadFile] = File(None),
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
) -> int:
    if file:
        file_path = get_unique_filename(file.filename)
        save_file(file, file_path)
    else:
        file_path = ""
    post_id = await save_post_to_db(session, user, post_title, file_path, incident_id)
    return post_id


@router.get("/all")
async def get_incidents(
        longitude: float,
        latitude: float,
        radius: float = Query(None, description="Радиус от точки в метрах"),
        session: AsyncSession = Depends(get_async_session)
) -> Sequence[IncidentReadModel]:
    raw_query = f"""SELECT *
        FROM incident as i
        WHERE (ST_DistanceSphere(
          ST_MakePoint(i.longitude, i.latitude),    
          ST_MakePoint({longitude}, {latitude})
        ) <= {radius}) AND (i.is_active = True OR i.is_predictive = True);"""
    query = select(Incident).from_statement(text(raw_query))
    incidents = await session.execute(query)
    incidents = incidents.scalars().all()
    return incidents


@router.put("/deactivate")
async def deactivate_incident(
        incident_id: int,
        response: Response,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    if user.is_superuser:
        await change_incident_status(incident_id, session, False)
    else:
        response.status_code = status.HTTP_403_FORBIDDEN


@router.get("/detail")
async def get_detail_incident(
        incident_id: int, session: AsyncSession = Depends(get_async_session)
) -> Sequence[PostReadModel]:
    raw_sql = text("""SELECT p.user_id, p.title,
               split_part(p.media_path, '/', -1) as media_path,
               p.created_at
               FROM post_incident as p
               WHERE incident_id = :incident_id""").bindparams(incident_id=incident_id)
    # query = select(PostIncident).from_statement(raw_sql)
    posts = await session.execute(raw_sql)
    posts = posts.mappings().all()
    return [PostReadModel(**post) for post in posts]


@router.get("/file")
async def download_media_for_incident(image_path: str):
    return FileResponse(POSTS_PATH / image_path)
