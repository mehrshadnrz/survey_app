from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app import schemas, crud
from app.dependencies import (
    get_current_user,
    check_existing_response,
    check_user_access_to_response,
    verify_response,
    viewable_response,
    verify_exam_session,
    verify_exam_author_by_session,
    get_current_admin_user,
)

router = APIRouter()


@router.post("/{exam_session_id}", response_model=schemas.ResponseResponse)
async def create_response(
    response: schemas.ResponseCreate,
    current_user: dict = Depends(get_current_user),
    exam_session: dict = Depends(verify_exam_session),
    existed_response: dict = Depends(check_existing_response),
):
    created_response = await crud.create_response(
        exam_session.id,
        current_user.id,
        response.startTime,
    )
    return created_response


@router.post("/private/{exam_session_id}", response_model=schemas.ResponseResponse)
async def create_private_response(
    response: schemas.PrivateResponseCreate,
    current_user: dict = Depends(verify_exam_author_by_session),
    exam_session: dict = Depends(verify_exam_session),
):
    created_response = await crud.create_response(
        exam_session.id, response.userId, None
    )
    return created_response


@router.put("/{exam_session_id}", response_model=schemas.ResponseResponse)
async def update_response(
    update_response=schemas.ResponseUpdate,
    current_user: dict = Depends(get_current_user),
    exam_session: dict = Depends(verify_exam_session),
    response: dict = Depends(verify_response),
):
    updated_response = await crud.update_response(response["id"], update_response)
    return updated_response


@router.get("/{exam_session_id}", response_model=schemas.ResponseWithAnswers)
async def get_response(response=Depends(check_user_access_to_response)):
    return response


@router.get(
    "/{exam_session_id}/user/{user_id}", response_model=schemas.ResponseWithAnswers
)
async def get_user_response(
    user_id: int,
    current_user: dict = Depends(verify_exam_author_by_session),
    exam_session: dict = Depends(verify_exam_session),
):
    response = await crud.get_response_by_session_and_user(exam_session.id, user_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )
    return response


@router.get("/exam/{exam_session_id}", response_model=List[schemas.ResponseResponse])
async def list_responses(
    current_user: dict = Depends(verify_exam_author_by_session),
    exam_session: dict = Depends(verify_exam_session),
):
    responses = await crud.list_responses_for_exam_session(exam_session.id)
    return responses


@router.post("/{exam_session_id}/add_answer", response_model=schemas.AnswerResponse)
async def create_answer(
    answer: schemas.AnswerCreate,
    response: dict = Depends(verify_response),
):
    answer_data = answer.dict()
    existed_answer = await crud.get_answer(response["id"], answer_data["questionId"])
    if existed_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Answer already exists",
        )
    created_answer = await crud.create_answer(response["id"], answer_data)
    return created_answer


@router.get("/{exam_session_id}/answers", response_model=List[schemas.AnswerResponse])
async def list_answers(
    response: dict = Depends(viewable_response),
):
    answers = await crud.list_answers_for_response(response["id"])
    return answers


@router.get(
    "/score/{exam_session_id}/user/{user_id}",
    response_model=schemas.ResponseWithScore,
)
async def get_user_response_with_score(
    user_id: int,
    current_user: dict = Depends(verify_exam_author_by_session),
    exam_session: dict = Depends(verify_exam_session),
):
    response = await crud.get_response_by_session_and_user(exam_session.id, user_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )
    return response


@router.post("/add_score/{answer_id}", response_model=schemas.AnswerResponse)
async def add_answer_score(
    answer_id: int,
    score: float,
    current_user: dict = Depends(get_current_admin_user),
):
    answer = await crud.get_answer_by_id(answer_id=answer_id)
    if answer.question.questionType not in ["SHORT_TEXT", "LONG_TEXT"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can not add score for this type of question",
        )
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found",
        )
    return await crud.save_score(
        answer_id=answer_id,
        score=score,
    )
