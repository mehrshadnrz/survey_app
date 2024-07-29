from prisma import Prisma
from app.auth import get_password_hash
from app.schemas import (
    Role,
    UserCreate,
    UserUpdate,
    SurveyCreate,
    SurveyUpdate,
    QuestionCreate,
    QuestionUpdate,
    QuestionResponse,
)


prisma = Prisma()


"""
User
"""
async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "identity_code": user.identity_code,
        "role": Role.USER.value
    }
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

async def create_admin(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "identity_code": user.identity_code,
        "role": Role.ADMIN.value
    }
    return await prisma.user.create(data=user_data)

async def update_user(user_id: int, user: UserUpdate):
    user_data = user.dict(exclude_unset=True)
    return await prisma.user.update(where={"id": user_id}, data=user_data)

async def list_admin_users():
    return await prisma.user.find_many(where={"role": Role.ADMIN.value})

async def list_users():
    return await prisma.user.find_many(where={"role": Role.USER.value})


"""
Survey
"""
async def create_survey(survey: SurveyCreate, user_id: int):
    survey_data = survey.dict()
    survey_data["authorId"] = user_id
    return await prisma.survey.create(data=survey_data)

async def get_survey_by_id(survey_id: int):
    return await prisma.survey.find_unique(where={"id": survey_id})

async def list_user_surveys(user_id: int):
    return await prisma.survey.find_many(where={"authorId": user_id})

async def update_survey(survey_id: int, survey: SurveyUpdate):
    update_data = survey.dict(exclude_unset=True)
    return await prisma.survey.update(where={"id": survey_id}, data=update_data)

async def delete_survey(survey_id: int):
    return await prisma.survey.delete(where={"id": survey_id})


"""
Question
"""
async def create_question(survey_id: int, question: QuestionCreate) -> QuestionResponse:
    question_data = question.dict(exclude={"options"})
    question_data['surveyId'] = survey_id
    created_question = await prisma.question.create(data=question_data)
    
    created_options = []
    for option in question.options:
        option_data = option.dict()
        option_data['questionId'] = created_question.id
        created_option = await prisma.option.create(data=option_data)
        created_options.append(created_option.dict())
    
    created_question_dict = created_question.dict()
    created_question_dict['options'] = created_options
    return created_question_dict

async def get_question_by_id(question_id: int):
    return await prisma.question.find_unique(
        where={"id": question_id},
        include={"options": True}
    )

async def list_survey_questions(survey_id: int):
    question_list = await prisma.question.find_many(
        where={"surveyId": survey_id},
        include={"options": True}
    )
    return question_list

async def update_question(question_id: int, question: QuestionUpdate):
    question_data = question.dict(exclude={"options"})
    updated_question = await prisma.question.update(
        where={"id": question_id},
        data=question_data
    )

    updated_options = []
    for option in question.options:
        option_data = option.dict(exclude_unset=True)
        updated_option = await prisma.option.update(
            where={"id": option.id},
            data=option_data
        )
        updated_options.append(updated_option.dict())

    updated_question_dict = updated_question.dict()
    updated_question_dict['options'] = updated_options
    return updated_question_dict

async def delete_question(question_id: int):
    to_delete_question = await prisma.question.find_unique(
        where={"id": question_id},
        include={"options": True}
    )
    await prisma.option.delete_many(where={"questionId": question_id})
    await prisma.question.delete(where={"id": question_id})

    return to_delete_question


"""
Response
"""
async def create_response(survey_id, user_id: int):
    response_data = {"surveyId": survey_id, "userId": user_id}
    return await prisma.response.create(data=response_data)

async def get_response_by_survey_and_user(survey_id: int, user_id: int):
    return await prisma.response.find_first(where={"surveyId": survey_id, "userId": user_id}, include={"answers": True})

async def list_responses_for_survey(survey_id: int):
    return await prisma.response.find_many(where={"surveyId": survey_id})


"""
Answer
"""
async def create_answer(response_id: int, answer_data: dict):
    answer_data['responseId'] = response_id
    return await prisma.answer.create(data=answer_data)

async def list_answers_for_response(response_id: int):
    return await prisma.answer.find_many(where={"responseId": response_id})

async def get_answer(response_id: int, question_id: int):
    return await prisma.answer.find_first(where={"responseId": response_id, "questionId": question_id})
