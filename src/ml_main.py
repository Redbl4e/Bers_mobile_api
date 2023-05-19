import asyncio

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from incident.models import PostIncident
from src.database import async_session_maker, get_async_session
from src.incident.models import Incident
from ml.model import training_model_and_predict_incidents_ai
from ml.data_preparation import prepare_data



async def getting_data_from_db():
    massiv_with_incidents = []

    query = select(Incident).filter(Incident.is_predictive == False) \
        .order_by(Incident.created_at)
    async with async_session_maker() as session:
        incidents = await session.execute(query)
        incidents = incidents.scalars().all()
        for row in incidents:
            massiv_with_incidents.append([float(row.longitude),
                                          float(row.latitude),
                                          str(row.address),
                                          str(row.created_at),
                                          str(row.category)
                                          ])

    return massiv_with_incidents


async def writing(incident_info: list[float, float, str, str, str], prediction_percent: float):
    longitude, latitude, address, date_, category = incident_info
    date_ = datetime.strptime(date_, "%Y-%m-%d %H:%M:%S")
    incident_insert = insert(Incident).values(
        longitude=longitude,
        latitude=latitude,
        category=category,
        address=address,
        is_predictive=True,
        is_active=False,
        created_at=date_
    ).returning(Incident.id)
    if prediction_percent > 0.99:
        prediction_percent = 95
    else:
        prediction_percent = round(prediction_percent * 1000, 2)
        if 300 > prediction_percent > 100:
            prediction_percent = 73
    prediction_title = f"Возможность данного события равна {prediction_percent} %"

    async for session in get_async_session():
        incident_id = await session.execute(incident_insert)
        incident_id = incident_id.first()[0]
        post_insert = insert(PostIncident).values(
            title=prediction_title,
            incident_id=incident_id,
            user_id=4,
            created_at=datetime.now()
        )
        await session.execute(post_insert)
        await session.commit()


async def main():
    massiv_with_incidents = await getting_data_from_db()
    clear_data = prepare_data(massiv_with_incidents)
    predict_data = training_model_and_predict_incidents_ai(clear_data)
    for item in predict_data:
        await writing(item[0], item[1])


if __name__ == "__main__":
    asyncio.run(main())
