from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import JobApplicationCreateModel, JobApplicationUpdateModel
from ..db.models import JobApplication, JobInterview
from sqlmodel import select, desc
from datetime import datetime
from typing import Optional
from sqlalchemy import or_, func
from sqlalchemy.sql.operators import ilike_op
import uuid
class JobApplicationService:
    async def get_all_jobs(self, session : AsyncSession, page: int = 1,page_size: int = 10,search: Optional[str] = None,status: Optional[str] = None):
        statement = select(JobApplication).where(JobApplication.deleted_at == None)
        
        if search:
            statement = statement.where(
                or_(
                    JobApplication.company_name.ilike(f"%{search}%"),  # type: ignore[attr-defined] # prefix search
                    JobApplication.job_title.ilike(f"%{search}%")# type: ignore[attr-defined]
                )
            )
        
        if status:
            statement = statement.where(JobApplication.status == status)
        
        offset = (page - 1) * page_size
        statement = statement.order_by(desc(JobApplication.created_at)).offset(offset).limit(page_size)

        result = await session.exec(statement)
        jobs = result.all()

        count_statement = select(func.count()).select_from(JobApplication).where(JobApplication.deleted_at == None)
        if search:
            count_statement = count_statement.where(
                or_(
                    JobApplication.company_name.ilike(f"{search}%"),# type: ignore[attr-defined]
                    JobApplication.job_title.ilike(f"{search}%")# type: ignore[attr-defined]
                )
            )
        if status:
            count_statement = count_statement.where(JobApplication.status == status)

        total_result = await session.exec(count_statement)
        total_count = total_result.one()

        return {
            "data": jobs,
            "page": page,
            "page_size": page_size,
            "total": total_count
        }
    
    async def get_user_jobs(self, user_id:str, session : AsyncSession, page: int = 1,page_size: int = 10,search: Optional[str] = None,status: Optional[str] = None):
        statement = select(JobApplication).where(JobApplication.user_uid == user_id,JobApplication.deleted_at == None)
        if search:
            statement = statement.where(
                or_(
                    JobApplication.company_name.ilike(f"%{search}%"),   # type: ignore[attr-defined]# prefix search
                    JobApplication.job_title.ilike(f"%{search}%") # type: ignore[attr-defined]
                )
            )
        
        if status:
            statement = statement.where(JobApplication.status == status)
        
        offset = (page - 1) * page_size
        statement = statement.order_by(desc(JobApplication.created_at)).offset(offset).limit(page_size)

        result = await session.exec(statement)
        jobs = result.all()

        count_statement = select(func.count()).select_from(JobApplication).where(JobApplication.deleted_at == None)
        if search:
            count_statement = count_statement.where(
                or_(
                    JobApplication.company_name.ilike(f"{search}%"),# type: ignore[attr-defined]
                    JobApplication.job_title.ilike(f"{search}%")# type: ignore[attr-defined]
                )
            )
        if status:
            count_statement = count_statement.where(JobApplication.status == status)

        total_result = await session.exec(count_statement)
        total_count = total_result.one()

        return {
            "data": jobs,
            "page": page,
            "page_size": page_size,
            "total": total_count
        }
        
    async def get_job(self, job_uid:str, session:AsyncSession):
        statement = select(JobApplication).where(JobApplication.id == job_uid, JobApplication.deleted_at is None)
        result = await session.exec(statement)
        job_application = result.first()
        return job_application if job_application is not None else None
    
    async def create_job(self, job_data:JobApplicationCreateModel,user_uid:uuid.UUID, session:AsyncSession):
        job_data_dict = job_data.model_dump()
        
        new_data = JobApplication(
            **job_data_dict
        )
        new_data.user_uid = user_uid
        session.add(new_data)
        
        await session.commit()
        
        return new_data
        
    
    async def update_job(self, job_uid:str, update_data:JobApplicationUpdateModel, session:AsyncSession):
        job_application_to_update = await self.get_job(job_uid, session)
        
        if job_application_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for key,value in update_data_dict.items():
                setattr(job_application_to_update,key,value)
            
            await session.commit()

            return job_application_to_update
        else :
            return None
    
    async def delete_job(self, job_uid:str, session:AsyncSession):
        job_application_to_delete = await self.get_job(job_uid, session)
        
        if job_application_to_delete is not None:
            job_application_to_delete.deleted_at = datetime.now()
            
            statement = select(JobInterview).where(
                JobInterview.job_application_id == job_uid,
                JobInterview.deleted_at == None
            )
            result = await session.exec(statement)
            interviews = result.all()

            for interview in interviews:
                interview.deleted_at = datetime.now()

            await session.commit()
            return job_application_to_delete
        else:
            return None