from fastapi import Depends, HTTPException, status
from app.schemas import Role
from app import auth, crud


async def get_current_user(token: str = Depends(auth.oauth2_scheme)):
    payload = auth.decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await crud.get_user_by_email(email=payload["sub"])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.role not in [Role.ADMIN.value, Role.SUPER_ADMIN.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Admin or Super Admin role required",
        )
    return current_user


async def get_current_super_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user.role != Role.SUPER_ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: Super Admin role required",
        )
    return current_user


async def verify_survey(
    survey_id: int,
):
    survey = await crud.get_survey_by_id(survey_id)
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Survey not found",
        )
    return survey


async def verify_author(
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(get_current_admin_user),
):
    if survey.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return current_user


async def verify_question(
    question_id: int,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    question = await crud.get_question_by_id(question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    if question.surveyId != survey.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return question


async def verify_option(
    option_id: int,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    option = await crud.get_option(option_id)
    if not option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Option not found"
        )
    question = await crud.get_question_by_id(option.questionId)
    if question.surveyId != survey.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return option


async def verify_impact(
    factor_impact_id: int,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    impact = await crud.get_factor_impact(factor_impact_id)
    if not impact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="FactorImpact not found"
        )
    option = await crud.get_option(impact.optionId)
    question = await crud.get_question_by_id(option.questionId)
    if question.surveyId != survey.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return impact


async def verify_static_option(
    static_option_id: int,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    static_option = await crud.get_static_option(static_option_id)
    if not static_option:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="StaticOption not found"
        )
    if static_option.surveyId != survey.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return static_option


async def verify_static_impact(
    static_factor_impact_id: int,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    static_impact = await crud.get_static_factor_impact(static_factor_impact_id)
    if not static_impact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="FactorImpact not found"
        )
    static_option = await crud.get_static_option(static_impact.staticOptionId)
    if static_option.surveyId != survey.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return static_impact


async def verify_exam(
    exam_id: int,
):
    exam = await crud.get_exam_by_id(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


async def verify_exam_author(
    exam: dict = Depends(verify_exam),
    current_user: dict = Depends(get_current_user),
):
    if exam.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return current_user


async def verify_exam_survey(
    exam_survey_id: int,
):
    exam_survey = await crud.get_exam_survey_by_id(exam_survey_id)
    if not exam_survey:
        raise HTTPException(status_code=404, detail="ExamSurvey not found")
    return exam_survey


async def verify_exam_session(
    exam_session_id: int,
):
    exam_session = await crud.get_exam_session_by_id(exam_session_id)
    if not exam_session:
        raise HTTPException(status_code=404, detail="ExamSession not found")
    return exam_session


async def verify_exam_author_by_session(
    exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(get_current_user),
):
    exam = await crud.get_exam_by_id(exam_id=exam_session.examId)
    if exam.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return current_user


async def check_existing_response(
    current_user: dict = Depends(get_current_user),
    exam_session: dict = Depends(verify_exam_session),
):
    existing_response = await crud.get_response_by_session_and_user(
        session_id=exam_session.id,
        user_id=current_user.id,
    )
    if existing_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Response already exists for this exam",
        )
    return existing_response


async def verify_response(
    exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(get_current_user),
):
    response = await crud.get_response_by_session_and_user(
        exam_session.id,
        current_user.id,
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )
    return response


async def viewable_response(
    current_user: dict = Depends(get_current_user),
    response: dict = Depends(verify_response),
    exam_session: dict = Depends(verify_exam_session),
):
    exam = await crud.get_exam_by_id(exam_id=exam_session.examId)
    if exam.viewableByAuthorOnly and exam.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return response


async def check_user_access_to_response(
    exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(get_current_user),
    response: dict = Depends(verify_response),
):
    exam = await crud.get_exam_by_id(exam_id=exam_session.examId)
    if response["userId"] != current_user.id and exam.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return response


async def check_user_access(
    exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(get_current_user),
):
    exam = await crud.get_exam_by_id(exam_id=exam_session.examId)
    response = await crud.get_response_by_session_and_user(
        exam_session.id,
        current_user.id,
    )
    if not response and exam.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return current_user
