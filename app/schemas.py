from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


# User
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


# Survey
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


# Option
class OptionBase(BaseModel):
    optionText: str

class OptionCreate(OptionBase):
    pass

class OptionUpdate(OptionBase):
    id : int

class OptionResponse(OptionBase):
    id: int
    questionId: int

    class Config:
        orm_mode: True


# Question
class QuestionBase(BaseModel):
    questionText: str
    questionType: str
    correctAnswer: Optional[str] = None

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


# Response
class ResponseBase(BaseModel):
    pass

class ResponseCreate(ResponseBase):
    pass

class ResponseResponse(ResponseBase):
    id: int
    surveyId: int
    userId: int
    responseDate: datetime

    class Config:
        orm_mode: True


# Answer
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
