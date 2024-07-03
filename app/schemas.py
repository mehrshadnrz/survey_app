from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# User
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class TokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str


# Survey
class SurveyBase(BaseModel):
    title: str
    description: str

class SurveyCreate(SurveyBase):
    pass

class SurveyUpdate(SurveyBase):
    title: Optional[str] = None
    description: Optional[str] = None

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
