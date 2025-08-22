from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime
import uuid
class Status(Enum):
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    REJECTED = "rejected"
    ACCEPTED = "accepted"

class JobApplication(BaseModel) :
    uid:Optional[uuid.UUID] = None
    job_title:str
    company_name:str
    location:str
    application_date:str
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