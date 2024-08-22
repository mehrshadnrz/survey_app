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
    FactorCreate,
    FactorUpdate,
    QuestionType,
    ExamCreate,
    ExamUpdate,
    ExamSessionCreate,
    ExamSessionUpdate,
    ExamSurveyCreate,
    ExamSurveyUpdate,
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
        "role": Role.USER.value,
    }
    return await prisma.user.create(data=user_data)


# TEMP
async def create_superadmin(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "identity_code": user.identity_code,
        "role": Role.SUPER_ADMIN.value,
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
        "role": Role.ADMIN.value,
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


async def get_survey_with_questions(survey_id: int):
    return await prisma.survey.find_unique(
        where={"id": survey_id},
        include={
            "questions": {
                "include": {
                    "options": True
                }
            }
        }
    )


async def list_user_surveys(user_id: int):
    return await prisma.survey.find_many(where={"authorId": user_id})


async def update_survey(survey_id: int, survey: SurveyUpdate):
    update_data = survey.dict(exclude_unset=True)
    return await prisma.survey.update(where={"id": survey_id}, data=update_data)


async def delete_survey(survey_id: int):
    return await prisma.survey.delete(where={"id": survey_id})


"""
Factor
"""


async def create_factor(factor: FactorCreate, survey_id: int):
    data = factor.dict()
    data["surveyId"] = survey_id
    return await prisma.factor.create(data=data)


async def get_factor_by_id(factor_id: int):
    return await prisma.factor.find_unique(where={"id": factor_id})


async def list_survey_factors(survey_id: int):
    return await prisma.factor.find_many(where={"surveyId": survey_id})


async def update_factor(factor_id: int, factor: FactorUpdate):
    update_data = factor.dict(exclude_unset=True)
    return await prisma.factor.update(where={"id": factor_id}, data=update_data)


async def delete_factor(factor_id: int):
    return await prisma.factor.delete(where={"id": factor_id})


"""
Question
"""


async def create_question(survey_id: int, question: QuestionCreate) -> QuestionResponse:
    question_data = question.dict(exclude={"options"})
    question_data["surveyId"] = survey_id
    created_question = await prisma.question.create(data=question_data)

    if question.questionType in ["SHORT_TEXT", "LONG_TEXT"]:
        return created_question

    created_options = []
    for option in question.options:
        option_data = option.dict(exclude={"factorImpacts"})
        option_data["questionId"] = created_question.id
        created_option = await prisma.option.create(data=option_data)
        created_option_dict = created_option.dict()

        if question.questionType == QuestionType.PSYCHOLOGY:
            created_impacts = []
            for impact in option.factorImpacts:
                impact_data = impact.dict()
                impact_data["optionId"] = created_option.id
                created_impact = await prisma.factorimpact.create(data=impact_data)
                created_impacts.append(created_impact.dict())

            created_option_dict["factorImpacts"] = created_impacts

        created_options.append(created_option_dict)

    created_question_dict = created_question.dict()
    created_question_dict["options"] = created_options
    return created_question_dict


async def get_question_by_id(question_id: int):
    return await prisma.question.find_unique(
        where={"id": question_id},
        include={
            "options": {
                "include": {
                    "factorImpacts": True,
                }
            }
        },
    )


async def list_survey_questions(survey_id: int):
    question_list = await prisma.question.find_many(
        where={"surveyId": survey_id},
        include={"options": {"include": {"factorImpacts": True}}},
    )
    return question_list


async def update_question(question_id: int, question: QuestionUpdate):
    question_data = question.dict(exclude_unset=True, exclude={"options"})
    updated_question = await prisma.question.update(
        where={"id": question_id}, data=question_data
    )

    if updated_question.questionType in ["SHORT_TEXT", "LONG_TEXT"]:
        return updated_question

    updated_options = []
    for option in question.options:
        option_data = option.dict(exclude_unset=True, exclude={"factorImpacts"})
        updated_option = await prisma.option.update(
            where={"id": option.id}, data=option_data
        )

        updated_option_dict = updated_option.dict()

        if question.questionType == QuestionType.PSYCHOLOGY:
            updated_impacts = []
            for impact in option.factorImpacts:
                impact_data = impact.dict(exclude_unset=True)
                updated_impact = await prisma.factorimpact.update(
                    where={"id": impact.id}, data=impact_data
                )
                updated_impacts.append(updated_impact.dict())
            updated_option_dict["factorImpacts"] = updated_impacts

        updated_options.append(updated_option_dict)

    updated_question_dict = updated_question.dict()
    updated_question_dict["options"] = updated_options
    return updated_question_dict


async def delete_question(question_id: int):
    to_delete_question = await prisma.question.find_unique(
        where={"id": question_id},
        include={"options": {"include": {"factorImpacts": True}}},
    )

    options = to_delete_question.options
    for option in options:
        await prisma.factorimpact.delete_many(where={"optionId": option.id})

    await prisma.option.delete_many(where={"questionId": question_id})
    await prisma.question.delete(where={"id": question_id})

    return to_delete_question


async def get_option(option_id: int):
    option = await prisma.option.find_unique(
        where={"id": option_id}, include={"factorImpacts": True}
    )
    return option


"""
Response
"""


async def create_response(session_id: int, user_id: int):
    response_data = {"examSessionId": session_id, "userId": user_id}
    return await prisma.response.create(data=response_data)


async def get_response_by_session_and_user(session_id: int, user_id: int):
    return await prisma.response.find_first(
        where={"examSessionId": session_id, "userId": user_id},
        include={"answers": True},
    )


async def list_user_responses(user_id: int):
    return await prisma.response.find_many(where={"userId": user_id})


async def list_responses_for_exam_session(session_id: int):
    return await prisma.response.find_many(where={"examSessionId": session_id})


"""
Answer
"""


async def create_answer(response_id: int, answer_data: dict):
    answer_data["responseId"] = response_id
    return await prisma.answer.create(data=answer_data)


async def list_answers_for_response(response_id: int):
    return await prisma.answer.find_many(where={"responseId": response_id})


async def get_answer(response_id: int, question_id: int):
    return await prisma.answer.find_first(
        where={"responseId": response_id, "questionId": question_id}
    )


"""
Exam
"""


async def create_exam(exam: ExamCreate, user_id: int):
    exam_data = exam.dict()
    exam_data["authorId"] = user_id
    return await prisma.exam.create(data=exam_data)


async def get_exam_by_id(exam_id: int):
    return await prisma.exam.find_unique(where={"id": exam_id})


async def get_exam_with_surveys(exam_id: int):
    return await prisma.exam.find_unique(
        where={"id": exam_id},
        include={"examSurveys": True},
    )


async def list_user_exams(user_id: int):
    return await prisma.exam.find_many(where={"authorId": user_id})


async def update_exam(exam_id: int, exam: ExamUpdate):
    update_data = exam.dict(exclude_unset=True)
    return await prisma.exam.update(where={"id": exam_id}, data=update_data)


async def delete_exam(exam_id: int):
    return await prisma.exam.delete(where={"id": exam_id})


"""
ExamSurvey
"""


async def create_exam_survey(
    exam_survey: ExamSurveyCreate, exam_id: int, survey_id: int
):
    exam_survey_data = exam_survey.dict()
    exam_survey_data["examId"] = exam_id
    exam_survey_data["surveyId"] = survey_id
    return await prisma.examsurvey.create(data=exam_survey_data)


async def get_exam_survey_by_id(exam_survey_id: int):
    return await prisma.examsurvey.find_unique(where={"id": exam_survey_id})


async def get_exam_survey_by_exam_and_survey(exam_id: int, survey_id: int):
    return await prisma.examsurvey.find_first(
        where={"examId": exam_id, "surveyId": survey_id}
    )


async def list_exam_surveys(exam_id: int):
    return await prisma.examsurvey.find_many(where={"examId": exam_id})


async def update_exam_survey(exam_survey_id: int, exam_survey: ExamSurveyUpdate):
    update_data = exam_survey.dict(exclude_unset=True)
    return await prisma.examsurvey.update(
        where={"id": exam_survey_id}, data=update_data
    )


async def delete_exam_survey(exam_survey_id: int):
    return await prisma.examsurvey.delete(where={"id": exam_survey_id})


"""
ExamSession
"""


async def create_exam_session(exam_session: ExamSessionCreate, exam_id: int):
    exam_session_data = exam_session.dict()
    exam_session_data["examId"] = exam_id
    return await prisma.examsession.create(data=exam_session_data)


async def get_exam_session_by_id(exam_session_id: int):
    return await prisma.examsession.find_unique(where={"id": exam_session_id})


async def list_exam_sessions(exam_id: int):
    return await prisma.examsession.find_many(where={"examId": exam_id})


async def update_exam_session(exam_session_id: int, exam_session: ExamSessionUpdate):
    update_data = exam_session.dict(exclude_unset=True)
    return await prisma.examsession.update(
        where={"id": exam_session_id}, data=update_data
    )


async def delete_exam_session(exam_session_id: int):
    return await prisma.examsession.delete(where={"id": exam_session_id})


async def list_public_exam_sessions():
    exam_sessions = await prisma.examsession.find_many(
        where={"exam": {"isPublic": True}},
        include={
            "exam": {
                "include": {
                    "examSurveys": True,
                }
            }
        },
    )
    return exam_sessions
