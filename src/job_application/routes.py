from fastapi import APIRouter, status, Depends
from src.job_application.schemas import JobApplicationUpdateModel, JobApplicationCreateModel
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from src.job_application.models import JobApplication
from sqlmodel.ext.asyncio.session import AsyncSession
from src.job_application.services import JobApplicationService
from src.auth.dependencies import AccessTokenBearer, RoleChecker

access_token_bearer = AccessTokenBearer()
job_application_router =  APIRouter()
job_application_service = JobApplicationService()
role_checker_standard = Depends(RoleChecker(['ADMIN', 'USER', 'GUEST']))
role_checker_admin = Depends(RoleChecker(['ADMIN']))

@job_application_router.get("/", response_model=list[JobApplication], dependencies=[role_checker_admin])
async def get_all_jobs(session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    job_applications = await job_application_service.get_all_jobs(session)
    return job_applications

@job_application_router.get("/user/{user_id}", response_model=list[JobApplication], dependencies=[role_checker_standard])
async def get_jobs_by_user_id(user_id:str,session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    job_applications = await job_application_service.get_user_jobs(user_id,session)
    return job_applications

@job_application_router.get("/{id}", dependencies=[role_checker_standard])
async def get_job_by_id(id:str, session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    job_application = await job_application_service.get_job(id, session)
    if job_application is not None :
        return job_application
    else :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

@job_application_router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobApplication, response_model_exclude_none=True, dependencies=[role_checker_standard])
async def create_job_application(job_data:JobApplicationCreateModel, session:AsyncSession = Depends(get_session), token_details:dict=Depends(access_token_bearer)) :
    user = token_details.get("user") if token_details else None
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = user["user_id"]
    
    job_application = await job_application_service.create_job(job_data,user_id, session)
    return job_application

@job_application_router.patch("/{id}", response_model_exclude_none=True, dependencies=[role_checker_standard])
async def update_job_application(id : str,job_data:JobApplicationUpdateModel,session:AsyncSession = Depends(get_session),token_details:dict=Depends(access_token_bearer)) :
    update_data = await job_application_service.update_job(id,job_data,session)
    
    if update_data:
        return update_data
    else :
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
@job_application_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker_standard])
async def delete_job_application(id:str,session:AsyncSession = Depends(get_session),token_details:dict=Depends(access_token_bearer) ) :
    delete_data = await job_application_service.delete_job(id,session)
    if delete_data:
        return None
    else :
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        ) 