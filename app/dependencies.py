from fastapi import Depends, HTTPException, status
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

async def get_survey_and_verify_user(survey_id: int, current_user: dict = Depends(get_current_user)):
    survey = await crud.get_survey_by_id(survey_id)
    if not survey or survey.authorId != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Survey not found or access denied",
        )
    return survey

async def get_question_and_verify_survey(question_id: int, survey: dict = Depends(get_survey_and_verify_user)):
    question = await crud.get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if question.surveyId != survey.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return question
