from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app import schemas, crud
from app.dependencies import (
    get_current_user,
    check_existing_response,
    check_user_access_to_response,
    verify_author,
    verify_survey,
)

router = APIRouter()


@router.post("/{survey_id}", response_model=schemas.ResponseResponse)
async def create_response(
    current_user: dict = Depends(get_current_user),
    survey: dict = Depends(verify_survey),
    dependencies=[
        Depends(check_existing_response),
    ]
):
    created_response = await crud.create_response(survey.id, current_user.id)
    return created_response


@router.get("/{survey_id}", response_model=schemas.ResponseResponse)
async def get_response(response=Depends(check_user_access_to_response)):
    return response


@router.get("/survey/{survey_id}", response_model=List[schemas.ResponseResponse])
async def list_responses(survey: dict = Depends(verify_author)):
    responses = await crud.list_responses_for_survey(survey.id)
    return responses


@router.post("/{survey_id}/add_answer", response_model=schemas.AnswerResponse)
async def create_answer(
    survey_id: int,
    answer: schemas.AnswerCreate,
    current_user: dict = Depends(get_current_user),
):
    response = await crud.get_response_by_survey_and_user(survey_id, current_user.id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )
    created_answer = await crud.create_answer(response.id, answer)
    return created_answer


@router.get("/{survey_id}/answers", response_model=List[schemas.AnswerResponse])
async def list_answers(survey_id: int, current_user: dict = Depends(get_current_user)):
    response = await crud.get_response_by_survey_and_user(survey_id, current_user.id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )
    answers = await crud.list_answers_for_response(response.id)
    return answers


@router.get(
    "/survey/{survey_id}/all_answers", response_model=List[schemas.AnswerResponse]
)
async def list_all_answers(
    survey_id: int, current_user: dict = Depends(get_current_user)
):
    survey = await crud.get_survey_by_id(survey_id)
    if not survey:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Survey not found",
        )
    if survey.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    responses = await crud.list_responses_for_survey(survey_id)
    all_answers = []
    for response in responses:
        answers = await crud.list_answers_for_response(response.id)
        all_answers.extend(answers)
    return all_answers
