from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from app import schemas, crud
from app.dependencies import (
    get_current_admin_user,
    verify_author,
    verify_question,
    verify_survey,
    verify_option,
    verify_impact,
    verify_static_option,
    verify_static_impact,
)

router = APIRouter()


@router.post("/", response_model=schemas.SurveyResponse)
async def create_survey(
    survey: schemas.SurveyCreate,
    current_user: dict = Depends(get_current_admin_user),
):
    created_survey = await crud.create_survey(survey, current_user.id)
    return created_survey


@router.get("/{survey_id}", response_model=schemas.SurveyResponse)
async def get_survey(
    survey: dict = Depends(verify_survey), current_user: dict = Depends(verify_author)
):
    return survey


@router.get("/", response_model=List[schemas.SurveyResponse])
async def list_surveys(current_user: dict = Depends(get_current_admin_user)):
    surveys = await crud.list_user_surveys(current_user.id)
    return surveys


@router.put("/{survey_id}", response_model=schemas.SurveyResponse)
async def update_survey(
    survey: schemas.SurveyUpdate,
    existing_survey: dict = Depends(verify_survey),
    currnet_user: dict = Depends(verify_author),
):
    if existing_survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not edit survey after activation",
        )
    updated_survey = await crud.update_survey(existing_survey.id, survey)
    return updated_survey


@router.delete("/{survey_id}", response_model=schemas.SurveyResponse)
async def delete_survey(
    existing_survey: dict = Depends(verify_survey),
    currnet_user: dict = Depends(verify_author),
):
    if existing_survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not delete survey after activation",
        )
    deleted_survey = await crud.delete_survey(existing_survey.id)
    return deleted_survey


@router.post("/{survey_id}/add_question", response_model=schemas.QuestionResponse)
async def create_question(
    question: schemas.QuestionCreate,
    survey=Depends(verify_survey),
    currnet_user: dict = Depends(verify_author),
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
    currnet_user: dict = Depends(verify_author),
):
    questions = await crud.list_survey_questions(survey.id)
    return questions


@router.put(
    "/{survey_id}/update_question/{question_id}",
    response_model=schemas.QuestionResponse,
)
async def update_question(
    survey_id: int,
    question: schemas.QuestionUpdate,
    existing_question=Depends(verify_question),
):
    existing_survey = await crud.get_survey_by_id(survey_id)
    if existing_survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not edit question after activation",
        )
    updated_question = await crud.update_question(existing_question.id, question)
    return updated_question


@router.delete(
    "/{survey_id}/delete_question/{question_id}",
    response_model=schemas.QuestionResponse,
)
async def delete_question(
    survey_id: int,
    question=Depends(verify_question),
):
    existing_survey = await crud.get_survey_by_id(survey_id)
    if existing_survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not delete question after activation",
        )
    deleted_question = await crud.delete_question(question.id)
    return deleted_question


@router.delete(
    "/{survey_id}/delete_option/{option_id}",
    response_model=schemas.OptionResponse,
)
async def delete_option(
    survey_id: int,
    option=Depends(verify_option),
):
    existing_survey = await crud.get_survey_by_id(survey_id)
    if existing_survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not delete option after activation",
        )
    deleted_option = await crud.delete_option(option.id)
    return deleted_option


@router.delete(
    "/{survey_id}/delete_factor_impact/{factor_impact_id}",
    response_model=schemas.FactorImpactResponse,
)
async def delete_factor_impact(
    survey_id: int,
    impact=Depends(verify_impact),
):
    existing_survey = await crud.get_survey_by_id(survey_id)
    if existing_survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not delete factor impact after activation",
        )
    deleted_impact = await crud.delete_factor_impact(impact.id)
    return deleted_impact


@router.post("/{survey_id}/factor/", response_model=schemas.FactorResponse)
async def create_factor(
    factor: schemas.FactorCreate,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    created_factor = await crud.create_factor(factor, survey.id)
    return created_factor


@router.get("/{survey_id}/factor/{factor_id}", response_model=schemas.FactorResponse)
async def get_factor(
    factor_id: int,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    factor = await crud.get_factor_by_id(factor_id)
    return factor


@router.get("/{survey_id}/factors/", response_model=List[schemas.FactorResponse])
async def list_factor(
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    factors = await crud.list_survey_factors(survey.id)
    return factors


@router.put("/{survey_id}/factor/{factor_id}", response_model=schemas.FactorResponse)
async def update_factor(
    factor_id: int,
    factor: schemas.FactorUpdate,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    if survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not update factor after activation",
        )
    updated_factor = await crud.update_factor(factor_id, factor)
    return updated_factor


@router.delete("/{survey_id}/factor/{factor_id}", response_model=schemas.FactorResponse)
async def delete_factor(
    factor_id: int,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    if survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not delete factor after activation",
        )
    factor = await crud.delete_factor(factor_id)
    return factor


@router.post("/{survey_id}/parameter/", response_model=schemas.ParameterResponse)
async def create_parameter(
    parameter: schemas.ParameterCreate,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    created_parameter = await crud.create_parameter(parameter, survey.id)
    return created_parameter


@router.get(
    "/{survey_id}/parameter/{parameter_id}",
    response_model=schemas.ParameterResponse,
)
async def get_parameter(
    parameter_id: int,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    parameter = await crud.get_parameter_by_id(parameter_id)
    return parameter


@router.get("/{survey_id}/parameter/", response_model=List[schemas.ParameterResponse])
async def list_parameter(
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    parameters = await crud.list_survey_parameters(survey.id)
    return parameters


@router.put(
    "/{survey_id}/parameter/{parameter_id}",
    response_model=schemas.ParameterResponse,
)
async def update_parameter(
    parameter_id: int,
    parameter: schemas.ParameterUpdate,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    if survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not update parameter after activation",
        )
    updated_parameter = await crud.update_parameter(parameter_id, parameter)
    return updated_parameter


@router.delete(
    "/{survey_id}/parameter/{parameter_id}",
    response_model=schemas.ParameterResponse,
)
async def delete_parameter(
    parameter_id: int,
    survey: dict = Depends(verify_survey),
    current_user: dict = Depends(verify_author),
):
    if survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not delete parameter after activation",
        )
    parameter = await crud.delete_parameter(parameter_id)
    return parameter


@router.post(
    "/{survey_id}/add_static_option", response_model=schemas.StaticOptionResponse
)
async def create_static_option(
    static_option: schemas.StaticOptionCreate,
    survey=Depends(verify_survey),
    currnet_user: dict = Depends(verify_author),
):
    new_static_option = await crud.create_static_option(survey.id, static_option)
    return new_static_option


@router.get(
    "/{survey_id}/get_static_option/{static_option_id}",
    response_model=schemas.StaticOptionResponse,
)
async def get_static_option(static_option=Depends(verify_static_option)):
    return static_option


@router.get(
    "/{survey_id}/list_static_options",
    response_model=List[schemas.StaticOptionResponse],
)
async def list_static_option(
    survey=Depends(verify_survey),
    currnet_user: dict = Depends(verify_author),
):
    static_options = await crud.list_static_options(survey.id)
    return static_options


@router.put(
    "/{survey_id}/update_static_option/{static_option_id}",
    response_model=schemas.StaticOptionResponse,
)
async def update_static_option(
    survey_id: int,
    static_option: schemas.StaticOptionUpdate,
    existing_static_option=Depends(verify_static_option),
):
    existing_survey = await crud.get_survey_by_id(survey_id)
    if existing_survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not edit static_option after activation",
        )
    updated_static_option = await crud.update_static_option(
        existing_static_option.id, static_option
    )
    return updated_static_option


@router.delete(
    "/{survey_id}/delete_static_option/{static_option_id}",
    response_model=schemas.StaticOptionResponse,
)
async def delete_static_option(
    survey_id: int,
    static_option=Depends(verify_static_option),
):
    existing_survey = await crud.get_survey_by_id(survey_id)
    if existing_survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not delete static_option after activation",
        )
    deleted_static_option = await crud.delete_static_option(static_option.id)
    return deleted_static_option


@router.delete(
    "/{survey_id}/delete_static_factor_impact/{static_factor_impact_id}",
    response_model=schemas.StaticFactorImpactResponse,
)
async def delete_static_factor_impact(
    survey_id: int,
    static_impact=Depends(verify_static_impact),
):
    existing_survey = await crud.get_survey_by_id(survey_id)
    if existing_survey.isActive is True:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can not delete static_factor impact after activation",
        )
    deleted_static_impact = await crud.delete_static_factor_impact(static_impact.id)
    return deleted_static_impact
