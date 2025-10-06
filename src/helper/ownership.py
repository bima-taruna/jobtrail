from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.models import JobApplication
import uuid

async def ensure_job_belongs_to_user(job_uid: str, user_id: uuid.UUID, session: AsyncSession) -> JobApplication:
    statement = select(JobApplication).where(
        JobApplication.id == job_uid,
        JobApplication.user_uid == user_id,
        JobApplication.deleted_at == None
    )
    result = await session.exec(statement)
    job_app = result.first()

    if not job_app:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this job application"
        )

    return job_app
