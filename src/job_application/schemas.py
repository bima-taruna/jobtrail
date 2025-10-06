from pydantic import BaseModel
from src.job_application.enums import Status
from typing import Optional, List
from datetime import datetime
from src.job_timeline.schemas import JobTimeline
from src.interview.schemas import JobInterview
import uuid


class JobApplication(BaseModel) :
    id:Optional[uuid.UUID] = None
    job_title:str
    company_name:str
    location:str
    application_date:datetime
    status : Status
    created_at:datetime
    updated_at:datetime
    deleted_at:Optional[datetime] =None
    
class JobApplicationCreateModel(BaseModel):
    job_title:str
    company_name:str
    location:str
    application_date:datetime
    status : Status
    
class JobApplicationUpdateModel(BaseModel) :
    job_title:Optional[str] = None
    company_name:Optional[str] = None
    location:Optional[str] = None
    application_date:Optional[datetime] = None
    status : Optional[Status] = None
    
    
class JobApplicationDetail(BaseModel):
    job_title:str
    company_name:str
    location:str
    application_date:datetime
    status : Status
    timelines: Optional[List[JobTimeline]] = []
    job_interviews: Optional[List[JobInterview]] = []
    