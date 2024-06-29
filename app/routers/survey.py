from fastapi import APIRouter, Depends
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
