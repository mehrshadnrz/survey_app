from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import crud
from app.routers import user, survey, response


app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(survey.router, prefix="/surveys", tags=["surveys"])
app.include_router(response.router, prefix="/responses", tags=["responses"])

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
