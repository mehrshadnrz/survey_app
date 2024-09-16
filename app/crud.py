from prisma import Prisma
from typing import List
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
    OptionCreate,
    OptionUpdate,
    ResponseUpdate,
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
        where={"id": survey_id}, include={"questions": {"include": {"options": True}}}
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
    async with prisma.tx() as transaction:
        question_data = question.dict(exclude={"options"})
        question_data["surveyId"] = survey_id
        created_question = await transaction.question.create(data=question_data)

        if question.questionType in ["SHORT_TEXT", "LONG_TEXT"]:
            return created_question

        created_options = await create_options_for_question(
            transaction, created_question.id, question
        )

        created_question_dict = created_question.dict()
        created_question_dict["options"] = created_options
        return created_question_dict


async def create_options_for_question(
    transaction, question_id: int, question: QuestionCreate
) -> List[dict]:
    created_options = []
    for option in question.options:
        option_data = option.dict(exclude={"factorImpacts"})
        option_data["questionId"] = question_id
        created_option = await transaction.option.create(data=option_data)
        created_option_dict = created_option.dict()

        if question.questionType == QuestionType.PSYCHOLOGY:
            created_impacts = await create_factor_impacts_for_option(
                transaction, created_option.id, option
            )
            created_option_dict["factorImpacts"] = created_impacts

        created_options.append(created_option_dict)

    return created_options


async def create_factor_impacts_for_option(
    transaction, option_id: int, option: OptionCreate
) -> List[dict]:
    created_impacts = []
    for impact in option.factorImpacts:
        impact_data = impact.dict(exclude={"factorImpacts", "id"})
        impact_data["optionId"] = option_id
        created_impact = await transaction.factorimpact.create(data=impact_data)
        created_impacts.append(created_impact.dict())

    return created_impacts


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
    async with prisma.tx() as transaction:
        question_data = question.dict(exclude_unset=True, exclude={"options"})
        updated_question = await transaction.question.update(
            where={"id": question_id}, data=question_data
        )

        if updated_question.questionType in ["SHORT_TEXT", "LONG_TEXT"]:
            return updated_question

        await update_options_for_question(transaction, updated_question.id, question)

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


async def update_options_for_question(
    transaction, question_id: int, question: QuestionUpdate
) -> List[dict]:
    updated_options = []
    for option in question.options:
        if option.id:
            option_data = option.dict(exclude_unset=True, exclude={"factorImpacts"})

            updated_option = await transaction.option.update(
                where={"id": option.id}, data=option_data
            )

            updated_option_dict = updated_option.dict()

            if question.questionType == QuestionType.PSYCHOLOGY:
                updated_impacts = await update_factor_impacts_for_option(
                    transaction, updated_option.id, option
                )
                updated_option_dict["factorImpacts"] = updated_impacts

            updated_options.append(updated_option_dict)
        else:
            option_data = option.dict(exclude={"factorImpacts", "id"})
            option_data["questionId"] = question_id
            created_option = await transaction.option.create(data=option_data)
            created_option_dict = created_option.dict()

            if question.questionType == QuestionType.PSYCHOLOGY:
                created_impacts = await create_factor_impacts_for_option(
                    transaction, created_option.id, option
                )
                created_option_dict["factorImpacts"] = created_impacts

            updated_options.append(created_option_dict)

    return updated_options


async def update_factor_impacts_for_option(
    transaction, option_id: int, option: OptionUpdate
) -> List[dict]:
    updated_impacts = []
    for impact in option.factorImpacts:
        if impact.id:
            impact_data = impact.dict(exclude_unset=True)
            updated_impact = await transaction.factorimpact.update(
                where={"id": impact.id}, data=impact_data
            )
            updated_impacts.append(updated_impact.dict())
        else:
            impact_data = impact.dict(exclude={"id"})
            impact_data["optionId"] = option_id
            created_impact = await transaction.factorimpact.create(data=impact_data)
            updated_impacts.append(created_impact.dict())

    return updated_impacts


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


async def get_factor_impact(factor_impact_id: int):
    impact = await prisma.factorimpact.find_unique(where={"id": factor_impact_id})
    return impact


async def delete_option(option_id: int):
    await prisma.factorimpact.delete_many(where={"optionId": option_id})
    return await prisma.option.delete(where={"id": option_id})


async def delete_factor_impact(impact_id: int):
    return await prisma.factorimpact.delete(where={"id": impact_id})


"""
Response
"""


async def create_response(session_id: int, user_id: int, startTime=None):
    response_data = {
        "examSessionId": session_id,
        "userId": user_id,
        "startTime": startTime,
    }
    return await prisma.response.create(data=response_data)


async def update_response(response_id: int, response: ResponseUpdate):
    update_data = response.dict()
    return await prisma.response.update(where={"id": response_id}, data=update_data)


async def get_response_by_session_and_user(session_id: int, user_id: int, check: bool = False):
    response = await prisma.response.find_first(
        where={"examSessionId": session_id, "userId": user_id},
        include={"answers": True},
    )
    
    if check:
        return response

    last_answer = await prisma.answer.find_first(
        where={"responseId": response.id}, order={"creationDate": "desc"}
    )
    response_dict = response.dict()
    response_dict["lastAnswer"] = last_answer
    return response_dict


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
    async with prisma.tx() as transaction:
        exam_data = exam.dict(exclude={"examSurveys"})
        exam_data["authorId"] = user_id

        created_exam = await transaction.exam.create(data=exam_data)

        for survey in exam.examSurveys:
            survey_data = survey.dict()
            survey_data["examId"] = created_exam.id
            await transaction.examsurvey.create(data=survey_data)

        return await transaction.exam.find_unique(
            where={"id": created_exam.id},
            include={
                "examSurveys": {
                    "include": {
                        "survey": True,
                    }
                }
            },
        )


async def get_exam_by_id(exam_id: int):
    return await prisma.exam.find_unique(
        where={"id": exam_id},
        include={
            "examSurveys": {
                "include": {
                    "survey": True,
                }
            }
        },
    )


async def get_exam_with_surveys(exam_id: int):
    return await prisma.exam.find_unique(
        where={"id": exam_id},
        include={
            "examSurveys": {
                "include": {
                    "survey": True,
                }
            }
        },
    )


async def list_user_exams(user_id: int):
    return await prisma.exam.find_many(
        where={"authorId": user_id},
        include={
            "examSurveys": {
                "include": {
                    "survey": True,
                }
            }
        },
    )


async def update_exam(exam_id: int, exam: ExamUpdate):
    async with prisma.tx() as transaction:
        update_data = exam.dict(exclude_unset=True, exclude={"examSurveys"})

        updated_exam = await transaction.exam.update(
            where={"id": exam_id}, data=update_data
        )

        if exam.examSurveys:
            for survey in exam.examSurveys:
                if survey.id:
                    await transaction.examsurvey.update(
                        where={"id": survey.id}, data=survey.dict(exclude_unset=True)
                    )
                else:
                    survey_data = survey.dict()
                    survey_data["examId"] = updated_exam.id
                    await transaction.examsurvey.create(data=survey_data)

        return await transaction.exam.find_unique(
            where={"id": updated_exam.id},
            include={
                "examSurveys": {
                    "include": {
                        "survey": True,
                    }
                }
            },
        )


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
    created_exam_survey = await prisma.examsurvey.create(data=exam_survey_data)
    return await prisma.examsurvey.find_unique(
        where={"id": created_exam_survey.id},
        include={"survey": True},
    )


async def get_exam_survey_by_id(exam_survey_id: int):
    return await prisma.examsurvey.find_unique(
        where={"id": exam_survey_id},
        include={"survey": True},
    )


async def get_exam_survey_by_exam_and_survey(exam_id: int, survey_id: int):
    return await prisma.examsurvey.find_first(
        where={"examId": exam_id, "surveyId": survey_id},
        include={"survey": True},
    )


async def list_exam_surveys(exam_id: int):
    return await prisma.examsurvey.find_many(
        where={"examId": exam_id},
        include={"survey": True},
    )


async def update_exam_survey(exam_survey_id: int, exam_survey: ExamSurveyUpdate):
    update_data = exam_survey.dict(exclude_unset=True)
    updated_exam_survey = await prisma.examsurvey.update(
        where={"id": exam_survey_id}, data=update_data
    )
    return await prisma.examsurvey.find_unique(
        where={"id": updated_exam_survey.id},
        include={"survey": True},
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
    return await prisma.examsession.find_unique(
        where={"id": exam_session_id},
        include={
            "exam": {
                "include": {
                    "examSurveys": {
                        "include": {
                            "survey": True,
                        }
                    }
                }
            }
        },
    )


async def list_exam_sessions(exam_id: int):
    return await prisma.examsession.find_many(
        where={"examId": exam_id},
        include={
            "exam": {
                "include": {
                    "examSurveys": {
                        "include": {
                            "survey": True,
                        }
                    }
                }
            }
        },
    )


async def update_exam_session(exam_session_id: int, exam_session: ExamSessionUpdate):
    update_data = exam_session.dict(exclude_unset=True)
    updated_session = prisma.examsession.update(
        where={"id": exam_session_id}, data=update_data
    )
    return await prisma.examsession.find_unique(
        where={"id": updated_session.id},
        include={
            "exam": {
                "include": {
                    "examSurveys": {
                        "include": {
                            "survey": True,
                        }
                    }
                }
            }
        },
    )


async def delete_exam_session(exam_session_id: int):
    return await prisma.examsession.delete(where={"id": exam_session_id})


async def list_public_exam_sessions():
    exam_sessions = await prisma.examsession.find_many(
        where={"exam": {"isPublic": True}},
        include={
            "exam": {
                "include": {
                    "examSurveys": {
                        "include": {
                            "survey": True,
                        }
                    }
                }
            }
        },
    )
    return exam_sessions
