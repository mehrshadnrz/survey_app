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
    current_user: dict = Depends(get_current_user),
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


async def check_existing_response(
    current_user: dict = Depends(get_current_user),
    survey: dict = Depends(verify_survey),
):
    existing_response = await crud.get_response_by_survey_and_user(
        survey.id, current_user.id
    )
    if existing_response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Response already exists for this survey",
        )
    return existing_response


async def verify_response(
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(get_current_user),
):
    response = await crud.get_response_by_survey_and_user(survey.id, current_user.id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )
    if survey.viewableByAuthorOnly and survey.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return response


async def check_user_access_to_response(
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(get_current_user),
    response: dict = Depends(verify_response),
):
    if response.userId != current_user.id and survey.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    return response


async def verify_exam(
    exam_id: int,
    current_user: dict = Depends(get_current_user),
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
    current_user: dict = Depends(get_current_user),
):
    exam_survey = await crud.get_exam_survey_by_id(exam_survey_id)
    if not exam_survey:
        raise HTTPException(status_code=404, detail="ExamSurvey not found")
    return exam_survey


async def verify_exam_session(
    exam_session_id: int,
    current_user: dict = Depends(get_current_user),
):
    exam_session = await crud.get_exam_session_by_id(exam_session_id)
    if not exam_session:
        raise HTTPException(status_code=404, detail="ExamSession not found")
    return exam_session
