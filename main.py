from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


from src.auth.auth import auth_backend, fastapi_users
from src.auth.database import User
from src.auth.schemas import UserRead, UserCreate


from src.file.router import router as router_file

app = FastAPI(
    title = 'Data storage'
)

app.include_router(router_file)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

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
