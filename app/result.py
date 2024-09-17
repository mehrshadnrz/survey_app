from app import schemas, crud


async def calculate_text_score(
    correct_text: str,
    user_answer: str,
    full_score: float,
) -> float:
    # Placeholder function for text score calculation
    # Implement the actual logic here
    return full_score if correct_text==user_answer else 0


async def response_with_score(response: schemas.ResponseWithAnswers):
    response = schemas.ResponseWithAnswers(**response)
    answers_with_score = []
    total_score = 0
    survey_factor_values = {}

    for answer in response.answers:
        question = await crud.get_question_by_id(question_id=answer.questionId)
        survey_id = question.surveyId

        if survey_id not in survey_factor_values:
            factors = await crud.list_survey_factors(survey_id=survey_id)
            survey_factor_values[survey_id] = {factor.id: {"name": factor.name, "value": 0} for factor in factors}

        factors = survey_factor_values[survey_id]
        question_type = question.questionType
        full_score = question.point

        score = 0

        if question_type == schemas.QuestionType.MULTIPLE_CHOICE:
            selected_option = await crud.get_option(option_id=answer.optionId)
            if question.correctOption == selected_option.order:
                score = full_score

        elif question_type in [
            schemas.QuestionType.LONG_TEXT,
            schemas.QuestionType.SHORT_TEXT,
        ]:
            score = await calculate_text_score(
                correct_text=question.correctAnswer,
                user_answer=answer.answerText,
                full_score=full_score,
            )

        elif question_type == schemas.QuestionType.PSYCHOLOGY:
            user_option = await crud.get_option(answer.optionId)
            factor_impacts = user_option.factorImpacts

            for factor_impact in factor_impacts:
                factor = await crud.get_factor_by_id(factor_impact.factorId)
                factor_id = factor.id

                if factor_impact.plus:
                    factors[factor_id]["value"] += factor_impact.impact
                else:
                    factors[factor_id]["value"] -= factor_impact.impact

        answer_with_score = answer.dict()
        answer_with_score["score"] = score
        answers_with_score.append(answer_with_score)
        total_score += score

    factors_with_value = []
    for survey_id, factors in survey_factor_values.items():
        for factor_id, factor_data in factors.items():
            factor_dict = {
                "id": factor_id,
                "surveyId": survey_id,
                "name": factor_data["name"],
                "value": factor_data["value"]
            }
            factors_with_value.append(factor_dict)

    response_with_score = response.dict()
    response_with_score["answers"] = answers_with_score
    response_with_score["totalScore"] = total_score
    response_with_score["factorValues"] = factors_with_value

    return response_with_score
