from app import schemas, crud


# TODO: Arvin bezan ino
async def calculate_text_score(
    correct_text,
    user_answer,
    full_score,
):
    return 0


async def response_with_score(response: schemas.ResponseWithAnswers):
    factors = await crud.list_survey_factors(survey_id=response.surveyId)
    factor_values = {factor.name : 0 for factor in factors}

    answers = response.answers

    answers_with_score = []

    total_score = 0
    for answer in answers:
        question = await crud.get_question_by_id(question_id=answer.questionId)
        question_type = question.questionType
        full_score = question.point

        score = 0

        if question_type == schemas.QuestionType.MULTIPLE_CHOICE:
            if question.correctOption.id == answer.optionId:
                score = full_score

        if question_type in [
            schemas.QuestionType.LONG_TEXT,
            schemas.QuestionType.SHORT_TEXT,
        ]:
            score = await calculate_text_score(
                correct_text=question.correctAnswer,
                user_answer=answer.answerText,
                full_score=full_score,
            )

        if question_type == schemas.QuestionType.PSYCOLOGY:
            user_option = await crud.get_option(answer.optionId)
            factor_impacts = user_option.factorImpacts

            for factor_impact in factor_impacts:
                factor = await crud.get_factor_by_id(factor_impact.factorId)

                if factor_impact.plus:
                    factor_values[factor.name] = (
                        factor_values[factor.name] + factor_impact.impact
                    )
                else:
                    factor_values[factor.name] = (
                        factor_values[factor.name] - factor_impact.impact
                    )

        answer_with_score = answer.dict()
        answer_with_score["score"] = score
        answers_with_score.append(answer_with_score)
        total_score = total_score + score

    factors_with_value = []
    for factor in factors:
        factor_dict = factor.dict()
        factor_dict["value"] = factor_values[factor.name]
        factors_with_value.append(factor_dict)

    response_with_score = response.dict()
    response_with_score["answers"] = answers_with_score
    response_with_score["total_score"] = total_score
    response_with_score["factorValues"] = factors_with_value

    return response_with_score
