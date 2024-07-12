from fastapi import APIRouter, Depends
from typing import List
from app import schemas, crud
from app.dependencies import (
    get_current_user,
    verify_author,
    verify_question,
    verify_survey,
)

router = APIRouter()


@router.post("/", response_model=schemas.SurveyResponse)
async def create_survey(
    survey: schemas.SurveyCreate, current_user: dict = Depends(get_current_user)
):
    created_survey = await crud.create_survey(survey, current_user.id)
    return created_survey


@router.get("/{survey_id}", response_model=schemas.SurveyResponse)
async def get_survey(
    survey: dict = Depends(verify_survey),
    dependencies=Depends(verify_author)
):
    return survey


@router.get("/", response_model=List[schemas.SurveyResponse])
async def list_surveys(current_user: dict = Depends(get_current_user)):
    surveys = await crud.list_user_surveys(current_user.id)
    return surveys


@router.put("/{survey_id}", response_model=schemas.SurveyResponse)
async def update_survey(
    survey: schemas.SurveyUpdate,
    existing_survey: dict = Depends(verify_survey),
    dependencies=Depends(verify_author)
):
    updated_survey = await crud.update_survey(existing_survey.id, survey)
    return updated_survey


@router.delete("/{survey_id}", response_model=schemas.SurveyResponse)
async def delete_survey(
    existing_survey: dict = Depends(verify_survey),
    dependencies=Depends(verify_author)
):
    deleted_survey = await crud.delete_survey(existing_survey.id)
    return deleted_survey


@router.post("/{survey_id}/add_question", response_model=schemas.QuestionResponse)
async def create_question(
    question: schemas.QuestionCreate,
    survey=Depends(verify_survey),
    dependencies=Depends(verify_author)
):
    new_question = await crud.create_question(survey.id, question)
    return new_question


@router.get(
    "/{survey_id}/get_question/{question_id}", response_model=schemas.QuestionResponse
)
async def get_question(question=Depends(verify_question)):
    return question


@router.get(
    "/{survey_id}/list_questions", response_model=List[schemas.QuestionResponse]
)
async def list_question(
    survey=Depends(verify_survey),
    dependencies=Depends(verify_author),
):
    questions = await crud.list_survey_questions(survey.id)
    return questions


@router.put(
    "/{survey_id}/update_question/{question_id}",
    response_model=schemas.QuestionResponse,
)
async def update_question(
    question: schemas.QuestionUpdate,
    existing_question=Depends(verify_question),
):
    updated_question = await crud.update_question(existing_question.id, question)
    return updated_question


@router.delete(
    "/{survey_id}/delete_question/{question_id}",
    response_model=schemas.QuestionResponse,
)
async def delete_question(question=Depends(verify_question)):
    deleted_question = await crud.delete_question(question.id)
    return deleted_question
