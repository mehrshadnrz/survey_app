from prisma import Prisma
from app.auth import get_password_hash
from app.schemas import (
    UserCreate,
    SurveyCreate,
    SurveyUpdate,
    QuestionCreate,
    QuestionUpdate,
)

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


# Question
async def create_question(survey_id: int, question: QuestionCreate):
    question_data = question.dict(exclude={"options"})
    question_data['surveyId'] = survey_id
    created_question = await prisma.question.create(data=question_data)

    for option in question.options:
        option_data = option.dict()
        option_data['questionId'] = created_question.id
        await prisma.option.create(data=option_data)

    return created_question

async def get_question_by_id(question_id: int):
    return await prisma.question.find_unique(
        where={"id": question_id},
        include={"options": True}
    )

async def list_survey_questions(survey_id: int):
    return await prisma.question.find_many(
        where={"surveyId": survey_id},
        include={"options": True}
    )

async def update_question(question_id: int, question: QuestionUpdate):
    question_data = question.dict(exclude={"options"})
    updated_question = await prisma.question.update(
        where={"id": question_id},
        data=question_data
    )

    # Update or create options
    for option in question.options:
        option_data = option.dict(exclude_unset=True)
        if option.id:
            await prisma.option.update(
                where={"id": option.id},
                data=option_data
            )
        else:
            option_data['questionId'] = question_id
            await prisma.option.create(data=option_data)

    return updated_question

async def delete_question(question_id: int):
    await prisma.option.delete_many(where={"questionId": question_id})
    deleted_question = await prisma.question.delete(where={"id": question_id})
    return deleted_question
