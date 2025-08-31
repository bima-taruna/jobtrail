from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Enum as PgEnum
import uuid
from .schemas import UserTypes
from datetime import datetime, date
from typing import Optional, List
from src.job_application import models
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
    job_applications: List["models.JobApplication"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self) -> str:
        return f"<User {self.username}>"