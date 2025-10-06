from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from src.job_application.enums import Status
import uuid


class JobApplicationEvent(str, Enum):
    SAVED = "SAVED"                
    APPLIED = "APPLIED"            
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    INTERVIEW_COMPLETED = "INTERVIEW_COMPLETED"
    OFFER_RECEIVED = "OFFER_RECEIVED"
    OFFER_ACCEPTED = "OFFER_ACCEPTED"
    OFFER_DECLINED = "OFFER_DECLINED"
    REJECTED = "REJECTED"            
    WITHDRAWN = "WITHDRAWN"
    
class JobTimeline(BaseModel) :
    id:Optional[uuid.UUID] = None
    event_type:JobApplicationEvent
    event_date:datetime
    notes:str
    created_at:datetime
    updated_at:datetime
    deleted_at:Optional[datetime] = None           

class JobTimelineCreateModel(BaseModel):
    event_type:JobApplicationEvent
    event_date:datetime
    notes:str

class JobTimelineUpdateModel(BaseModel):
    event_type:Optional[JobApplicationEvent] = None
    event_date:Optional[datetime] = None
    notes:Optional[str] = None

STATUS_TO_EVENT = {
    Status.SAVED: JobApplicationEvent.SAVED,
    Status.APPLIED: JobApplicationEvent.APPLIED,
    Status.INTERVIEWED: JobApplicationEvent.INTERVIEW_COMPLETED,
    Status.OFFERED: JobApplicationEvent.OFFER_RECEIVED,
    Status.ACCEPTED: JobApplicationEvent.OFFER_ACCEPTED,
    Status.REJECTED: JobApplicationEvent.REJECTED,
}

EVENT_TO_STATUS = {
    JobApplicationEvent.SAVED: Status.SAVED,
    JobApplicationEvent.APPLIED: Status.APPLIED,
    JobApplicationEvent.INTERVIEW_SCHEDULED: Status.INTERVIEWED,
    JobApplicationEvent.INTERVIEW_COMPLETED: Status.INTERVIEWED,
    JobApplicationEvent.OFFER_RECEIVED: Status.OFFERED,
    JobApplicationEvent.OFFER_ACCEPTED: Status.ACCEPTED,
    JobApplicationEvent.OFFER_DECLINED: Status.REJECTED,
    JobApplicationEvent.REJECTED: Status.REJECTED,
    JobApplicationEvent.WITHDRAWN: Status.WITHDRAWN, 
}