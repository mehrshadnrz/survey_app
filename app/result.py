from typing import List
from app import schemas, crud


async def calculate_score(
        question: schemas.QuestionResponse,
        answer: schemas.AnswerResponse,
    ):
    if question.questionType == schemas.QuestionType.MULTIPLE_CHOICE:
        user_choice = answer.optionId
        correct_choice = question.correctOption  # TODO: bugged
        point = question.point if user_choice==correct_choice else 0
        return point



async def answers_with_score(answers: List[schemas.AnswerResponse]):
    answers_with_score = []
    for answer in answers:
        question = crud.get_question_by_id(answer.questionId)




async def response_with_score(response: schemas.ResponseWithAnswers):
    answers = answers_with_score(response.answers)
    