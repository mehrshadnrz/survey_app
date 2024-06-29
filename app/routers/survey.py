from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app import schemas, crud
from app.dependencies import get_current_user, get_survey_and_verify_user

router = APIRouter()

@router.post("/", response_model=schemas.SurveyResponse)
async def create_survey(survey: schemas.SurveyCreate, current_user: dict = Depends(get_current_user)):
    created_survey = await crud.create_survey(survey, current_user.id)
    return created_survey

@router.get("/{survey_id}", response_model=schemas.SurveyResponse)
async def get_survey(survey: dict = Depends(get_survey_and_verify_user)):
    return survey

@router.get("/", response_model=List[schemas.SurveyResponse])
async def list_surveys(current_user: dict = Depends(get_current_user)):
    surveys = await crud.list_user_surveys(current_user.id)
    return surveys

@router.put("/{survey_id}", response_model=schemas.SurveyResponse)
async def update_survey(survey: schemas.SurveyUpdate, existing_survey: dict = Depends(get_survey_and_verify_user)):
    updated_survey = await crud.update_survey(existing_survey.id, survey)
    return updated_survey

@router.delete("/{survey_id}", response_model=schemas.SurveyResponse)
async def delete_survey(existing_survey: dict = Depends(get_survey_and_verify_user)):
    deleted_survey = await crud.delete_survey(existing_survey.id)
    return deleted_survey

@router.post("/{survey_id}/add_question", response_model=schemas.QuestionResponse)
async def create_question(
    survey_id: int, question: schemas.QuestionCreate, survey=Depends(get_survey_and_verify_user)
):
    new_question = await crud.create_question(survey.id, question)
    return new_question

@router.get("/{survey_id}/get_question/{question_id}", response_model=schemas.QuestionResponse)
async def get_question(
    survey_id: int, question_id: int, survey=Depends(get_survey_and_verify_user)
):
    existing_question = await crud.get_question_by_id(question_id)
    if not existing_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if existing_question.surveyId != survey.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return existing_question

@router.get("/{survey_id}/list_questions", response_model=schemas.QuestionResponse)
async def list_question(
    survey_id: int, survey=Depends(get_survey_and_verify_user)
):
    return await crud.list_survey_questions(survey.id)

@router.put("/{survey_id}/update_question/{question_id}", response_model=schemas.QuestionResponse)
async def update_question(
    survey_id: int, question_id: int, question: schemas.QuestionUpdate, survey=Depends(get_survey_and_verify_user)
):
    existing_question = await crud.get_question_by_id(question_id)
    if not existing_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if existing_question.surveyId != survey.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    updated_question = await crud.update_question(question_id, question)
    return updated_question

@router.delete("/{survey_id}/delete_question/{question_id}", response_model=schemas.QuestionResponse)
async def delete_question(
    survey_id: int, question_id: int, survey=Depends(get_survey_and_verify_user)
):
    existing_question = await crud.get_question_by_id(question_id)
    if not existing_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if existing_question.surveyId != survey.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    deleted_question = await crud.delete_question(question_id)
    return deleted_question