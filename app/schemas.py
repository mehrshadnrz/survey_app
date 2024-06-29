from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# User
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
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
