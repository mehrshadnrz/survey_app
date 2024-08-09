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
# TODO: isActive, duration
class SurveyBase(BaseModel):
    title: str
    description: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    isPublic: bool = False
    viewableByAuthorOnly: Optional[bool] = False

class SurveyCreate(SurveyBase):
    pass

class SurveyUpdate(SurveyBase):
    title: Optional[str] = None
    description: Optional[str] = None
    isPublic: Optional[bool] = None
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
# TODO: order
class OptionBase(BaseModel):
    optionText: str
    image: Optional[str] = None

class OptionCreate(OptionBase):
    factorImpacts: Optional[List[FactorImpactCreate]]

class OptionUpdate(OptionBase):
    id : int
    factorImpacts: Optional[List[FactorImpactUpdate]]

class OptionResponse(OptionBase):
    id: int
    questionId: int
    factorImpacts: Optional[List[FactorImpactResponse]]

    class Config:
        orm_mode: True


"""
Question
"""
# TODO: order, score, fix correctAnswer
class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    TEXT_INPUT = "TEXT_INPUT"
    RATING = "RATING"
    FILE_UPLOAD = "FILE_UPLOAD"
    DATE_PICKER = "DATE_PICKER"
    PSYCOLOGY = "PSYCOLOGY"

class QuestionBase(BaseModel):
    questionText: str
    correctAnswer: Optional[str] = None
    image: Optional[str] = None
    questionType: QuestionType

class QuestionCreate(QuestionBase):
    options: List[OptionCreate]

class QuestionUpdate(QuestionBase):
    options: List[OptionUpdate]

class QuestionResponse(QuestionBase):
    id: int
    surveyId: int
    options: Optional[List[OptionResponse]]

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
    surveyId: int
    userId: int
    responseDate: datetime

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
