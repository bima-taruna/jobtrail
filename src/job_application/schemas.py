from pydantic import BaseModel
from enum import Enum

class Status(Enum):
    SAVED = "saved"
    APPLIED = "applied"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    REJECTED = "rejected"
    ACCEPTED = "accepted"

class JobApplication(BaseModel) :
    id:int
    job_title:str
    company_name:str
    location:str
    application_date:str
    status : Status
    
class UpdateJobApplication(BaseModel) :
    job_title:str
    company_name:str
    location:str
    application_date:str
    status : Status