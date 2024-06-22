from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import crud
from app.routers import user

app = FastAPI()

app.include_router(user.router)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await crud.prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await crud.prisma.disconnect()
