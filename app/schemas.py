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


class SurveyCreate(SurveyBase):
    pass


class SurveyUpdate(SurveyBase):
    title: Optional[str] = None
    description: Optional[str] = None
    isActive: Optional[bool] = None


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
    parameterId: Optional[int] = None   


class FactorCreate(FactorBase):
    pass


class FactorUpdate(FactorBase):
    id: Optional[int] = None  
    name: Optional[str] = None  


class FactorResponse(FactorBase):
    id: int
    surveyId: int

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
    id: Optional[int] = None


class FactorImpactResponse(FactorImpactBase):
    id: int
    optionId: int

    class Config:
        orm_mode: True


"""
Factor Value
"""


class FactorValueBase(BaseModel):
    factorId: int
    responseId: int
    value: float = 0


class FactorValueCreate(FactorValueBase):
    pass


class FactorValueResponse(FactorValueBase):
    id: int

    class Config:
        orm_mode: True    


"""
Parameter
"""


class ParameterBase(BaseModel):
    name: str


class ParameterCreate(ParameterBase):
    factors: Optional[List[FactorCreate]] = None


class ParameterUpdate(ParameterBase):
    name: Optional[str] = None
    factors: Optional[List[FactorUpdate]] = None


class ParameterResponse(ParameterBase):
    id: int
    factors: Optional[List[FactorResponse]] = None

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
    id: Optional[int] = None
    optionText: Optional[str] = None
    order: Optional[int] = None
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
    OPENING = "OPENING"
    ENDING = "ENDING"


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


class QuestionResponseAbstract(BaseModel):
    id: int
    order: int

    class Config:
        orm_mode: True


class SurveyListQuestions(SurveyBase):
    id: int
    creationDate: datetime
    authorId: int
    questions: List[QuestionResponseAbstract]

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
    creationDate: datetime
    optionId: Optional[int] = None
    answerText: Optional[str] = None

    class Config:
        orm_mode: True


class AnswerResponseWithScore(BaseModel):
    id: int
    responseId: int
    questionId: int
    creationDate: datetime
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
    startTime: Optional[datetime] = None


class PrivateResponseCreate(ResponseBase):
    userId: int


class ResponseUpdate(ResponseBase):
    startTime: Optional[datetime] = None


class ResponseResponse(ResponseBase):
    id: int
    examSessionId: int
    userId: int
    responseDate: datetime
    totalScore: Optional[float] = None
    startTime: Optional[datetime] = None
    lastAnswer: Optional[AnswerResponse] = None

    class Config:
        orm_mode: True


class ResponseWithAnswers(ResponseBase):
    id: int
    examSessionId: int
    userId: int
    responseDate: datetime
    totalScore: Optional[float] = None
    startTime: Optional[datetime] = None
    answers: List[AnswerResponse]
    factorValues: Optional[List[AnswerResponse]] = None
    lastAnswer: Optional[AnswerResponse] = None

    class Config:
        orm_mode: True


class ResponseWithScore(ResponseBase):
    id: int
    examSessionId: int
    userId: int
    responseDate: datetime
    startTime: Optional[datetime] = None
    answers: List[AnswerResponseWithScore]
    totalScore: Optional[float] = None
    factorValues: Optional[List[FactorValueResponse]] = None
    lastAnswer: Optional[AnswerResponse] = None

    class Config:
        orm_mode: True


"""
ExamSurvey
"""


class ExamSurveyBase(BaseModel):
    surveyId: int
    order: int


class ExamSurveyCreate(ExamSurveyBase):
    pass


class ExamSurveyUpdate(ExamSurveyBase):
    id: Optional[int] = None
    surveyId: Optional[int] = None
    order: Optional[int] = None


class ExamSurveyResponse(ExamSurveyBase):
    id: int
    examId: int
    survey: Optional[SurveyResponse] = None

    class Config:
        orm_mode: True


"""
Exam
"""


class ExamBase(BaseModel):
    title: str
    description: str
    isPublic: bool = True
    isActive: bool = False
    viewableByAuthorOnly: bool = False


class ExamCreate(ExamBase):
    examSurveys: List[ExamSurveyCreate]


class ExamUpdate(ExamBase):
    title: Optional[str] = None
    description: Optional[str] = None
    isPublic: Optional[bool] = None
    isActive: Optional[bool] = None
    viewableByAuthorOnly: Optional[bool] = None
    examSurveys: Optional[List[ExamSurveyUpdate]] = None


class ExamResponse(ExamBase):
    id: int
    authorId: int
    examSurveys: Optional[List[ExamSurveyResponse]] = None

    class Config:
        orm_mode: True


"""
ExamSession
"""


class ExamSessionBase(BaseModel):
    startTime: datetime
    endTime: Optional[datetime]
    duration: Optional[int] = None  # in minutes
    timerOnQuestion: Optional[bool] = False


class ExamSessionCreate(ExamSessionBase):
    pass


class ExamSessionUpdate(ExamSessionBase):
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    duration: Optional[int] = None


class ExamSessionResponse(ExamSessionBase):
    id: int
    examId: int
    exam: Optional[ExamResponse] = None

    class Config:
        orm_mode: True
