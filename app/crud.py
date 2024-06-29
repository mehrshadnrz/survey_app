from prisma import Prisma
from app.schemas import UserCreate, SurveyCreate, SurveyUpdate
from app.auth import get_password_hash

prisma = Prisma()

# User
async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = {"username": user.username, "email": user.email, "password": hashed_password}
    return await prisma.user.create(data=user_data)

async def get_user_by_email(email: str):
    return await prisma.user.find_unique(where={"email": email})

async def get_user_by_username(username: str):
    return await prisma.user.find_unique(where={"username": username})

async def get_user(user_id: int):
    return await prisma.user.find_unique(where={"id": user_id})

async def get_user_by_email_or_username(identifier: str):
    user = await get_user_by_email(identifier)
    if not user:
        user = await get_user_by_username(identifier)
    return user


# Survey
async def create_survey(survey: SurveyCreate, user_id: int):
    return await prisma.survey.create(data={"title": survey.title, "description": survey.description, "authorId": user_id})

async def get_survey_by_id(survey_id: int):
    return await prisma.survey.find_unique(where={"id": survey_id})

async def list_user_surveys(user_id: int):
    return await prisma.survey.find_many(where={"authorId": user_id})

async def update_survey(survey_id: int, survey: SurveyUpdate):
    update_data = survey.dict(exclude_unset=True)
    return await prisma.survey.update(where={"id": survey_id}, data=update_data)

async def delete_survey(survey_id: int):
    return await prisma.survey.delete(where={"id": survey_id})
