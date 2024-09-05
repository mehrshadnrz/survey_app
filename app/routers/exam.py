from fastapi import APIRouter, Depends
from typing import List
from app import schemas, crud
from app.dependencies import (
    get_current_admin_user,
    get_current_user,
    verify_exam_author,
    verify_exam,
    verify_exam_survey,
    verify_exam_session,
    check_user_access,
)


router = APIRouter()


"""
Exam
"""


@router.post("/", response_model=schemas.ExamResponse)
async def create_exam(
    exam: schemas.ExamCreate,
    current_user: dict = Depends(get_current_admin_user),
):
    created_exam = await crud.create_exam(exam, current_user.id)
    return created_exam


@router.get("/{exam_id}", response_model=schemas.ExamResponse)
async def get_exam(
    exam: dict = Depends(verify_exam),
    current_user: dict = Depends(verify_exam_author),
):
    return exam


@router.get("/", response_model=List[schemas.ExamResponse])
async def list_exams(
    current_user: dict = Depends(get_current_admin_user),
):
    exams = await crud.list_user_exams(current_user.id)
    return exams


@router.put("/{exam_id}", response_model=schemas.ExamResponse)
async def update_exam(
    exam: schemas.ExamUpdate,
    existing_exam: dict = Depends(verify_exam),
    current_user: dict = Depends(verify_exam_author),
):
    updated_exam = await crud.update_exam(existing_exam.id, exam)
    return updated_exam


@router.delete("/{exam_id}", response_model=schemas.ExamResponse)
async def delete_exam(
    existing_exam: dict = Depends(verify_exam),
    current_user: dict = Depends(verify_exam_author),
):
    deleted_exam = await crud.delete_exam(existing_exam.id)
    return deleted_exam


"""
ExamSurvey
"""


@router.get(
    "/{exam_id}/survey/{exam_survey_id}", response_model=schemas.ExamSurveyResponse
)
async def get_exam_survey(
    exam_survey: dict = Depends(verify_exam_survey),
    current_user: dict = Depends(verify_exam_author),
):
    return exam_survey


@router.get("/{exam_id}/survey/", response_model=List[schemas.ExamSurveyResponse])
async def list_exam_surveys(
    exam: dict = Depends(verify_exam),
    current_user: dict = Depends(verify_exam_author),
):
    exam_surveys = await crud.list_exam_surveys(exam.id)
    return exam_surveys


@router.delete(
    "/{exam_id}/survey/{exam_survey_id}", response_model=schemas.ExamSurveyResponse
)
async def delete_exam_survey(
    existing_exam_survey: dict = Depends(verify_exam_survey),
    current_user: dict = Depends(verify_exam_author),
):
    deleted_exam_survey = await crud.delete_exam_survey(existing_exam_survey.id)
    return deleted_exam_survey


"""
ExamSession
"""


@router.post("/{exam_id}/session/", response_model=schemas.ExamSessionResponse)
async def create_exam_session(
    exam_session: schemas.ExamSessionCreate,
    current_user: dict = Depends(verify_exam_author),
    exam: dict = Depends(verify_exam),
):
    created_exam_session = await crud.create_exam_session(exam_session, exam.id)
    return created_exam_session


@router.get(
    "/{exam_id}/session/{exam_session_id}", response_model=schemas.ExamSessionResponseWithExam
)
async def get_exam_session(
    exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(verify_exam_author),
):
    return exam_session


@router.get("/{exam_id}/session/", response_model=List[schemas.ExamSessionResponseWithExam])
async def list_exam_sessions(
    exam: dict = Depends(verify_exam),
    current_user: dict = Depends(verify_exam_author),
):
    exam_sessions = await crud.list_exam_sessions(exam.id)
    return exam_sessions


@router.put(
    "/{exam_id}/session/{exam_session_id}", response_model=schemas.ExamSessionResponse
)
async def update_exam_session(
    exam_session: schemas.ExamSessionUpdate,
    existing_exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(verify_exam_author),
):
    updated_exam_session = await crud.update_exam_session(
        existing_exam_session.id, exam_session
    )
    return updated_exam_session


@router.delete(
    "/{exam_id}/session/{exam_session_id}", response_model=schemas.ExamSessionResponse
)
async def delete_exam_session(
    existing_exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(verify_exam_author),
):
    deleted_exam_session = await crud.delete_exam_session(existing_exam_session.id)
    return deleted_exam_session


@router.get(
    "/public/{exam_session_id}",
    response_model=schemas.ExamSessionResponseWithExam,
)
async def get_public_exam_session(
    exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(get_current_user),
):
    exam = await crud.get_exam_with_surveys(exam_session.examId)
    exam_session_dict = exam_session.dict()
    exam_session_dict["exam"] = exam
    return exam_session_dict


@router.get("/public/", response_model=List[schemas.ExamSessionResponseWithExam])
async def list_public_exam_sessions(
    current_user: dict = Depends(get_current_user),
):
    exam_sessions = await crud.list_public_exam_sessions()
    return exam_sessions


@router.get(
    "/private/{exam_session_id}",
    response_model=schemas.ExamSessionResponseWithExam,
)
async def get_private_exam_session(
    exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(check_user_access),
):
    exam = await crud.get_exam_with_surveys(exam_session.examId)
    exam_session_dict = exam_session.dict()
    exam_session_dict["exam"] = exam
    return exam_session_dict


@router.get(
    "/session/user/",
    response_model=list[schemas.ExamSessionResponseWithExam],
)
async def list_user_sessions(
    current_user: dict = Depends(get_current_user),
):
    responses = await crud.list_user_responses(current_user.id)

    sessions = []
    for response in responses:
        session = await crud.get_exam_session_by_id(response.examSessionId)
        sessions.append(session)

    return sessions


@router.get(
    "/session/",
    response_model=list[schemas.ExamSessionResponseWithExam],
)
async def list_sessions(
    current_user: dict = Depends(get_current_admin_user),
):
    exams = await crud.list_user_exams(current_user.id)

    sessions_list = []
    for exam in exams:
        sessions = await crud.list_exam_sessions(exam_id=exam.id)
        sessions_list.extend(sessions)

    return sessions_list


@router.get(
    "/session/{exam_session_id}/list_questions/",
    response_model=List[schemas.QuestionResponse],
)
async def get_question(
    exam_session: dict = Depends(verify_exam_session),
    current_user: dict = Depends(check_user_access),
):
    exam = await crud.get_exam_with_surveys(exam_id=exam_session.examId)

    questions = []
    for exam_survey in exam.examSurveys:
        survey = await crud.get_survey_with_questions(survey_id=exam_survey.surveyId)
        questions.extend(survey.questions)

    return questions
