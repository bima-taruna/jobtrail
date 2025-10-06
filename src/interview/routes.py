from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer, RoleChecker, get_current_user
from .service import JobInterviewService
from src.db.models import JobInterview, User
from .schemas import JobInterviewCreateModel,JobInterviewUpdateModel

access_token_bearer = AccessTokenBearer()
job_interview_router = APIRouter(
    prefix="/job-applications/{job_application_id}/interviews",
    tags=["Job Interviews"]
)
job_interview_service = JobInterviewService()
role_checker_standard = Depends(RoleChecker(['ADMIN', 'USER', 'GUEST']))
role_checker_admin = Depends(RoleChecker(['ADMIN']))

@job_interview_router.get("/", response_model=list[JobInterview], dependencies=[role_checker_standard])
async def get_all_job_interviews(job_application_id:str,session:AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    job_interviews =  await job_interview_service.get_all_interviews_by_app_id(job_application_id, current_user.id,session)
    return job_interviews

@job_interview_router.get("/{job_interview_id}", response_model=JobInterview, dependencies=[role_checker_standard])
async def get_job_interview_by_id(job_application_id:str, job_interview_id:str, session:AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)):
    job_interview = job_interview_service.get_interviews_by_id(job_application_id,job_interview_id,current_user.id,session)
    if job_interview is not None :
        return job_interview
    else :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="interview not found"
        )

@job_interview_router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobInterview, response_model_exclude_none=True, dependencies=[role_checker_standard])
async def create_job_application(job_application_id,interview_data:JobInterviewCreateModel, session:AsyncSession = Depends(get_session),current_user: User = Depends(get_current_user) ) :
    job_interview = await job_interview_service.create_job_interview(interview_data,job_application_id, current_user.id, session)
    return job_interview

@job_interview_router.patch("/{interview_id}", response_model_exclude_none=True, dependencies=[role_checker_standard])
async def update_job_application(job_application_id:str,job_interview_id : str,update_data:JobInterviewUpdateModel,session:AsyncSession = Depends(get_session),current_user: User = Depends(get_current_user)) :
    update_interview_data = await job_interview_service.update_job_interview(job_application_id,job_interview_id,current_user.id,update_data,session)
    
    if update_interview_data:
        return update_data
    else :
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

@job_interview_router.delete("/{interview_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker_standard])
async def delete_job_application(job_application_id:str,interview_id:str,session:AsyncSession = Depends(get_session),current_user: User = Depends(get_current_user) ) :
    delete_data = await job_interview_service.delete_job_interview(job_application_id, interview_id, current_user.id, session)
    if delete_data:
        return None
    else :
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        ) 
