from enum import Enum
from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from src.job_application.schemas import JobApplication
class UserTypes(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    GUEST = "GUEST"


class UserCreateModel(BaseModel):
    username:str = Field(max_length=25)
    first_name:str = Field(max_length=25)
    last_name:str = Field(max_length=25)
    email:str= Field(max_length=40)
    password:str= Field(max_length=25)
    
class UserModel(BaseModel):
    id: uuid.UUID 
    username: str
    password_hash:str = Field(exclude=True)
    email: str
    first_name:str
    last_name:str
    is_verified:bool 
    user_type:UserTypes
    created_at:datetime 
    updated_at:datetime
    
class UserJobAppsModel(UserModel):
    job_applications:List[JobApplication]

class UserLoginModel(BaseModel) :
    email: str = Field(max_length=40)
    password: str = Field(max_length=25)
    
