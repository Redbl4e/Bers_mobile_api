from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.config import fastapi_users, auth_backend
from auth.schemas import UserRead, UserCreate
from incident.router import router as incident_router

app = FastAPI(
    title="Будь в курсе"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"]
)

app.include_router(
    incident_router
)

# Поменять
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
