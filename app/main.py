import shutil
import os
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app import crud, dependencies
from app.routers import user, survey, response


app = FastAPI()


# Path to store uploaded images
UPLOAD_DIR = "uploads/"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

# TODO: make it one api in create question
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...), current_user: dict = Depends(dependencies.get_current_user)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

# TODO: make it one api in get and list question
@app.get("/images/{filename}")
async def get_image(filename: str, current_user: dict = Depends(dependencies.get_current_user)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)


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
