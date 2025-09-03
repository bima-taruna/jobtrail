from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime
import uuid

class JobInterviewType(Enum):
    PHONE = 'phone'
    VIDEO = 'video'
    ONSITE = 'onsite'
    
class JobInterview(BaseModel):
    id:Optional[uuid.UUID] = None
    interview_type:JobInterviewType
    interview_date:datetime
    interviewer_name:str
    notes:str
    created_at:datetime
    updated_at:datetime
    deleted_at:Optional[datetime] = None
    
class JobInterviewCreateModel(BaseModel):
    interview_type:JobInterviewType
    interview_date:datetime
    interviewer_name:str
    notes:str

class JobInterviewUpdateModel(BaseModel):
    interview_type:Optional[JobInterviewType]
    interview_date:Optional[datetime]
    interviewer_name:Optional[str]
    notes:Optional[str]