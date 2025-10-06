import uuid
from sqlmodel import select,desc
from sqlmodel.ext.asyncio.session import AsyncSession
from src.helper.ownership import ensure_job_belongs_to_user
from ..db.models import JobTimeline, JobApplication
from datetime import datetime
from src.job_timeline.schemas import JobTimelineCreateModel, JobTimelineUpdateModel, EVENT_TO_STATUS, STATUS_TO_EVENT

class JobTimelineService:
    async def get_all_timelines_by_app_id(self, job_application_id:str,user_id:uuid.UUID,session:AsyncSession):
       await ensure_job_belongs_to_user(job_application_id, user_id, session)
       statement = select(JobTimeline).where(JobTimeline.job_application_id == job_application_id, JobTimeline.deleted_at == None).order_by(desc(JobTimeline.event_date))
       result = await session.exec(statement)
       return result.all()
   
    async def get_timelines_by_id(self, job_application_id:str,job_timeline_id:str, user_id:uuid.UUID,session:AsyncSession):
        await ensure_job_belongs_to_user(job_application_id, user_id, session)
        statement = select(JobTimeline).where(JobTimeline.job_application_id == job_application_id, JobTimeline.id == job_timeline_id, JobTimeline.deleted_at == None)
        result = await session.exec(statement)
        job_timeline = result.first()
        return job_timeline if job_timeline is not None else None
    
    async def create_job_timeline(self, timeline_data:JobTimelineCreateModel, job_application_id:uuid.UUID, user_id:uuid.UUID, session:AsyncSession):
        await ensure_job_belongs_to_user(str(job_application_id),user_id, session)
        job_timeline_dict = timeline_data.model_dump()

        new_data = JobTimeline(
            **job_timeline_dict
        )
        
        new_data.job_application_id = job_application_id
        session.add(new_data)

        new_status = EVENT_TO_STATUS.get(new_data.event_type)
        if new_status :
            job_app = await session.get(JobApplication, job_application_id)
            if job_app:
                job_app.status = new_status
        
        await session.commit()
        await session.refresh(new_data)    
        return new_data
    
    async def update_job_timeline(self, job_application_id:str, job_timeline_id:str, user_id:uuid.UUID,update_data:JobTimelineUpdateModel,session: AsyncSession):
        job_timeline_to_update = await self.get_timelines_by_id(job_application_id,job_timeline_id, user_id,session)
        if job_timeline_to_update is not None:
            update_data_dict = update_data.model_dump(exclude_unset=True)
            for key,value in update_data_dict.items():
                setattr(job_timeline_to_update,key,value)
            
            if "event_type" in update_data_dict:
                new_status = EVENT_TO_STATUS.get(job_timeline_to_update.event_type)
                if new_status:
                    job_app = await session.get(JobApplication, job_application_id)
                    if job_app:
                        job_app.status = new_status
            
            await session.commit()
            return job_timeline_to_update
        else:
            return None
    
    async def delete_job_timeline(self, job_application_id:str, job_timeline_id:str, user_id:uuid.UUID, session:AsyncSession):
        job_timeline_to_delete = await self.get_timelines_by_id(job_application_id, job_timeline_id, user_id,session)
        if job_timeline_to_delete is not None:
        
            job_timeline_to_delete.deleted_at = datetime.now()
            
            statement = (
                select(JobTimeline)
                .where(
                    JobTimeline.job_application_id == job_application_id,
                    JobTimeline.deleted_at == None
                )
                .order_by(desc(JobTimeline.event_date))
            )
            result = await session.exec(statement)
            latest_event = result.first()
            if latest_event:
                new_status = EVENT_TO_STATUS.get(latest_event.event_type)
                if new_status:
                    job_app = await session.get(JobApplication, job_application_id)
                    if job_app:
                        job_app.status = new_status
            await session.commit()
            return job_timeline_to_delete
        else:
            return None