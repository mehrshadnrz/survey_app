from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app import schemas, crud
from app.dependencies import (
    get_current_user,
    check_existing_response,
    check_user_access_to_response,
    verify_author,
    verify_survey,
    verify_response
)

router = APIRouter()


@router.post("/{survey_id}", response_model=schemas.ResponseResponse)
async def create_response(
    current_user: dict = Depends(get_current_user),
    survey: dict = Depends(verify_survey),
    response: dict = Depends(check_existing_response),
):
    created_response = await crud.create_response(survey.id, current_user.id)
    return created_response


@router.post("/private/{survey_id}", response_model=schemas.ResponseResponse)
async def create_private_response(
    response: schemas.PrivateResponseCreate,
    current_user: dict = Depends(verify_author),
    survey: dict = Depends(verify_survey),
    check_response: dict = Depends(check_existing_response),
):
    created_response = await crud.create_response(survey.id, response.userId)
    return created_response


@router.get("/{survey_id}", response_model=schemas.ResponseResponse)
async def get_response(response=Depends(check_user_access_to_response)):
    return response


@router.get("/survey/{survey_id}", response_model=List[schemas.ResponseResponse])
async def list_responses(
    current_user: dict = Depends(verify_author), 
    survey: dict = Depends(verify_survey)
):
    responses = await crud.list_responses_for_survey(survey.id)
    return responses


@router.post("/{survey_id}/add_answer", response_model=schemas.AnswerResponse)
async def create_answer(
    survey_id: int,
    answer: schemas.AnswerCreate,
    current_user: dict = Depends(get_current_user), # check if needed
    response: dict = Depends(verify_response),
):
    answer_data = answer.dict()
    existed_answer = await crud.get_answer(response.id, answer_data["questionId"])
    if existed_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Answer already exists",
        )
    created_answer = await crud.create_answer(response.id, answer_data)
    return created_answer


@router.get("/{survey_id}/answers", response_model=List[schemas.AnswerResponse])
async def list_answers(
    survey_id: int,
    current_user: dict = Depends(get_current_user),
    response: dict = Depends(verify_response),
):
    answers = await crud.list_answers_for_response(response.id)
    return answers

# TODO: calculate score APIs and ...
