from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from src.job_application.schemas import Status
from datetime import datetime, date
from typing import Optional
import uuid

class JobApplication(SQLModel, table=True) :
    __tablename__ = "job_application" # type: ignore[assignment]
    id: uuid.UUID = Field(
        sa_column=Column(
          pg.UUID,
          nullable=False,
          primary_key=True,
          default=uuid.uuid4  
        )
    )
    job_title:str
    company_name:str
    location:str
    application_date:date
    status : Status
    created_at:datetime =  Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    deleted_at: Optional[datetime] = None


    def __repr__(self) -> str:
        return f"<JobApplication {self.job_title}"