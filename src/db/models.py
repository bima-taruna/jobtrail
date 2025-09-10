from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from src.job_application.schemas import Status
from src.interview.schemas import JobInterviewType
from sqlalchemy.orm import Mapped
from datetime import datetime, date
from typing import Optional, List
from src.auth.schemas import UserTypes
from sqlalchemy import Enum as PgEnum
import uuid

class JobApplication(SQLModel, table=True) :
    model_config = {"arbitrary_types_allowed": True} # type: ignore[assignment]
    __tablename__ = "job_application" # type: ignore[assignment]
    id: uuid.UUID = Field(
        sa_column=Column(
          pg.UUID,
          nullable=False,
          primary_key=True,
          default=uuid.uuid4  
        )
    )
    job_title:str = Field(index=True)
    company_name:str = Field(index=True)
    location:str
    application_date:date = Field(index=True)
    status : Status = Field(index=True, default=Status.APPLIED)
    user_uid:Optional[uuid.UUID] = Field(index=True,default=None, foreign_key="users.id")
    created_at:datetime =  Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    deleted_at: Optional[datetime] = Field(index=True, default=None)
    user: Optional["User"] = Relationship(back_populates="job_applications")
    job_interviews: List["JobInterview"] = Relationship(back_populates="job_application", sa_relationship_kwargs={"lazy":"selectin"})


    def __repr__(self) -> str:
        return f"<JobApplication {self.job_title}"


class User(SQLModel, table=True) :
    __tablename__ = 'users' # type: ignore[assignment]
    id: uuid.UUID = Field(
        sa_column=Column(
          pg.UUID,
          nullable=False,
          primary_key=True,
          default=uuid.uuid4  
        )
    )
    username: str
    password_hash:str = Field(exclude=True)
    email: str
    first_name:str
    last_name:str
    is_verified:bool = Field(default=False)
    user_type:UserTypes = Field(
        sa_column=Column(PgEnum(UserTypes, name="user_type"), nullable=False, server_default="USER")
    )
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    job_applications: List["JobApplication"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class JobInterview(SQLModel, table=True):
    __tablename__ = "job_interviews" # type: ignore[assignment]
    id: uuid.UUID = Field(
        sa_column=Column(
          pg.UUID,
          nullable=False,
          primary_key=True,
          default=uuid.uuid4  
        )
    )
    job_application_id:Optional[uuid.UUID] = Field(default=None, foreign_key="job_application.id")
    interview_type:JobInterviewType
    interview_date:date
    interviewer_name:str
    notes:str
    created_at:datetime =  Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    deleted_at: Optional[datetime] = None

    job_application: Optional["JobApplication"] = Relationship(back_populates="job_interviews")
    
    def __repr__(self) -> str:
        return f"<JobInterview {self.interview_type}>"