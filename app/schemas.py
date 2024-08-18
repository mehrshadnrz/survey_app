from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


"""
User
"""


class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str
    identity_code: str


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    identity_code: Optional[str]


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: str
    identity_code: str
    role: Role

    class Config:
        orm_mode: True


class TokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str
    role: Role


"""
Survey
"""


class SurveyBase(BaseModel):
    title: str
    description: str
    viewableByAuthorOnly: Optional[bool] = False


class SurveyCreate(SurveyBase):
    pass


class SurveyUpdate(SurveyBase):
    title: Optional[str] = None
    description: Optional[str] = None
    viewableByAuthorOnly: Optional[bool] = None


class SurveyResponse(SurveyBase):
    id: int
    creationDate: datetime
    authorId: int

    class Config:
        orm_mode: True


"""
Factor
"""


class FactorBase(BaseModel):
    name: str


class FactorCreate(FactorBase):
    pass


class FactorUpdate(FactorBase):
    pass


class FactorResponse(FactorBase):
    id: int
    surveyId: int

    class Config:
        orm_mode: True


class FactorValue(FactorBase):
    id: int
    surveyId: int
    value: int = 0

    class Config:
        orm_mode: True


"""
Factor Impact
"""


class FactorImpactBase(BaseModel):
    factorId: int
    impact: int
    plus: bool


class FactorImpactCreate(FactorImpactBase):
    pass


class FactorImpactUpdate(FactorImpactBase):
    id: int


class FactorImpactResponse(FactorImpactBase):
    id: int
    optionId: int

    class Config:
        orm_mode: True


"""
Option
"""


class OptionBase(BaseModel):
    optionText: str
    order: int
    image: Optional[str] = None


class OptionCreate(OptionBase):
    factorImpacts: Optional[List[FactorImpactCreate]] = None


class OptionUpdate(OptionBase):
    id: int
    factorImpacts: Optional[List[FactorImpactUpdate]] = None


class OptionResponse(OptionBase):
    id: int
    questionId: int
    factorImpacts: Optional[List[FactorImpactResponse]]

    class Config:
        orm_mode: True


"""
Question
"""


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    SHORT_TEXT = "SHORT_TEXT"
    LONG_TEXT = "LONG_TEXT"
    PSYCHOLOGY = "PSYCHOLOGY"


class QuestionBase(BaseModel):
    questionText: str
    correctAnswer: Optional[str] = None
    correctOption: Optional[int] = None  # based on order, not optionId
    image: Optional[str] = None
    order: int
    point: Optional[float] = None
    questionType: QuestionType


class QuestionCreate(QuestionBase):
    options: Optional[List[OptionCreate]] = None


class QuestionUpdate(QuestionBase):
    options: Optional[List[OptionUpdate]] = None
    questionText: Optional[str] = None
    order: Optional[int] = None
    questionType: Optional[QuestionType] = None


class QuestionResponse(QuestionBase):
    id: int
    surveyId: int
    options: Optional[List[OptionResponse]]

    class Config:
        orm_mode: True


"""
Answer
"""


class AnswerCreate(BaseModel):
    questionId: int
    optionId: Optional[int] = None
    answerText: Optional[str] = None


class AnswerResponse(BaseModel):
    id: int
    responseId: int
    questionId: int
    optionId: Optional[int] = None
    answerText: Optional[str] = None

    class Config:
        orm_mode: True


class AnswerResponseWithScore(BaseModel):
    id: int
    responseId: int
    questionId: int
    optionId: Optional[int] = None
    answerText: Optional[str] = None
    score: Optional[float] = None

    class Config:
        orm_mode: True


"""
Response
"""


class ResponseBase(BaseModel):
    pass


class ResponseCreate(ResponseBase):
    pass


class PrivateResponseCreate(ResponseBase):
    userId: int


class ResponseResponse(ResponseBase):
    id: int
    examSessionId: int
    userId: int
    responseDate: datetime

    class Config:
        orm_mode: True


class ResponseWithAnswers(ResponseBase):
    id: int
    examSessionId: int
    userId: int
    responseDate: datetime
    answers: List[AnswerResponse]

    class Config:
        orm_mode: True


class ResponseWithScore(ResponseBase):
    id: int
    examSessionId: int
    userId: int
    responseDate: datetime
    answers: List[AnswerResponseWithScore]
    totalScore: Optional[float] = None
    factorValues: Optional[List[FactorValue]] = None

    class Config:
        orm_mode: True


"""
Exam
"""


class ExamBase(BaseModel):
    title: str
    description: str
    isPublic: bool = True
    isActive: bool = True
    viewableByAuthorOnly: bool = False


class ExamCreate(ExamBase):
    pass


class ExamUpdate(ExamBase):
    title: Optional[str] = None
    description: Optional[str] = None
    isPublic: Optional[bool] = None
    isActive: Optional[bool] = None
    viewableByAuthorOnly: Optional[bool] = None


class ExamResponse(ExamBase):
    id: int
    authorId: int

    class Config:
        orm_mode: True


"""
ExamSurvey
"""


class ExamSurveyBase(BaseModel):
    order: int


class ExamSurveyCreate(ExamSurveyBase):
    pass


class ExamSurveyUpdate(ExamSurveyBase):
    order: Optional[int] = None


class ExamSurveyResponse(ExamSurveyBase):
    id: int
    examId: int
    surveyId: int

    class Config:
        orm_mode: True


"""
ExamSession
"""


class ExamSessionBase(BaseModel):
    startTime: datetime
    endTime: Optional[datetime]
    duration: Optional[int] = None  # in minutes


class ExamSessionCreate(ExamSessionBase):
    pass


class ExamSessionUpdate(ExamSessionBase):
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    duration: Optional[int] = None


class ExamSessionResponse(ExamSessionBase):
    id: int
    examId: int

    class Config:
        orm_mode: True


class ExamSessionResponseWithExam(ExamSessionBase):
    id: int
    exam: ExamResponse

    class Config:
        orm_mode: True