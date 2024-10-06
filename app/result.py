from app import schemas, crud


async def save_answer_scores_in_db(response: schemas.ResponseWithAnswers):
    response = schemas.ResponseWithAnswers(**response)

    surveys = []

    for answer in response.answers:
        question = await crud.get_question_by_id(question_id=answer.questionId)

        survey_id = question.surveyId

        if survey_id not in surveys:
            factors = await crud.list_survey_factors(survey_id=survey_id)

            for factor in factors:
                
                existing_factor_value = await crud.get_factor_value_by_factor_and_response(
                    factor_id=factor.id,
                    response_id=response.id
                )

                if not existing_factor_value:
                    factor_value = schemas.FactorValueCreate(
                        factorId=factor.id,
                        responseId=response.id,
                    )
                    await crud.create_factor_value(factor_value=factor_value)

            surveys.append(survey_id)

        if question.questionType == schemas.QuestionType.MULTIPLE_CHOICE:
            score = 0
            selected_option = await crud.get_option(option_id=answer.optionId)
            if question.correctOption == selected_option.order:
                score = question.point
            await crud.save_score(answer_id=answer.id, score=score)

        elif question.questionType == schemas.QuestionType.PSYCHOLOGY:
            user_option = await crud.get_option(answer.optionId)
            factor_impacts = user_option.factorImpacts

            for factor_impact in factor_impacts:
                factor_value = await crud.get_factor_value_by_factor_and_response(
                    factor_id=factor_impact.factorId,
                    response_id=response.id,
                )

                value = factor_value.value
                if factor_impact.plus:
                    value += factor_impact.impact
                else:
                    value -= factor_impact.impact

                await crud.update_factor_value(
                    factor_id=factor_impact.factorId,
                    response_id=response.id,
                    value=value,
                )


async def save_total_answer_in_db(response: schemas.ResponseWithAnswers):
    response = schemas.ResponseWithAnswers(**response)
    total_score = 0
    for answer in response.answers:
        if answer.score:
            total_score += answer.score

    if total_score != 0:
        await crud.save_total_score(
            response_id=response.id,
            total_score=total_score,
        )
