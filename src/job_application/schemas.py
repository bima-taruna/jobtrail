from pydantic import BaseModel
from enum import Enum
from typing import Optional

class Status(Enum):
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    REJECTED = "rejected"
    ACCEPTED = "accepted"

class JobApplication(BaseModel) :
    id:Optional[int] = None
    job_title:str
    company_name:str
    location:str
    application_date:str
    status : Status
    
class UpdateJobApplication(BaseModel) :
    job_title:Optional[str] = None
    company_name:Optional[str] = None
    location:Optional[str] = None
    application_date:Optional[str] = None
    status : Optional[Status] = None