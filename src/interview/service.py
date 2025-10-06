from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .schemas import JobInterviewCreateModel, JobInterviewUpdateModel
from ..db.models import JobInterview
from datetime import datetime
from src.helper.ownership import ensure_job_belongs_to_user
import uuid
class JobInterviewService:
    async def get_all_interviews_by_app_id(self, job_application_id:str, user_id:uuid.UUID, session: AsyncSession):
        await ensure_job_belongs_to_user(job_application_id, user_id, session)
        statement = select(JobInterview).where(JobInterview.job_application_id == job_application_id, JobInterview.deleted_at == None).order_by(desc(JobInterview.interview_date))
        result = await session.exec(statement)
        return result.all()

    async def get_interviews_by_id(self, job_application_id:str,job_interview_id:str, user_id:uuid.UUID,session:AsyncSession):
        await ensure_job_belongs_to_user(job_application_id, user_id, session)
        statement = select(JobInterview).where(JobInterview.job_application_id == job_application_id, JobInterview.id == job_interview_id, JobInterview.deleted_at == None)
        result = await session.exec(statement)
        job_interview = result.first()
        return job_interview if job_interview is not None else None
    
    async def create_job_interview(self, interview_data:JobInterviewCreateModel, job_application_id:uuid.UUID, user_id:uuid.UUID, session:AsyncSession):
        await ensure_job_belongs_to_user(str(job_application_id),user_id, session)
        job_interview_dict = interview_data.model_dump()
        
        new_data = JobInterview(
            **job_interview_dict
        )
        
        new_data.job_application_id = job_application_id
        session.add(new_data)
        await session.commit()
        return new_data
    
    async def update_job_interview(self, job_application_id:str, job_interview_id:str, user_id:uuid.UUID,update_data:JobInterviewUpdateModel,session: AsyncSession):
        job_interview_to_update = await self.get_interviews_by_id(job_application_id,job_interview_id, user_id,session)
        if job_interview_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for key,value in update_data_dict.items():
                setattr(job_interview_to_update,key,value)

            await session.commit()
            return job_interview_to_update
        else:
            return None
    
    async def delete_job_interview(self, job_application_id:str, job_interview_id:str, user_id:uuid.UUID, session:AsyncSession):
        job_interview_to_delete = await self.get_interviews_by_id(job_application_id, job_interview_id, user_id,session)
        if job_interview_to_delete is not None:
            job_interview_to_delete.deleted_at = datetime.now()
            await session.commit()
            return job_interview_to_delete
        else:
            return None