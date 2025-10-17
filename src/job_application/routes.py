from fastapi import APIRouter, status, Depends, Query
from src.job_application.schemas import JobApplicationUpdateModel, JobApplicationCreateModel, JobApplicationDetail, JobApplication
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from src.db.models import User, JobApplication as JobApplicationModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.job_application.services import JobApplicationService
from src.auth.dependencies import AccessTokenBearer, RoleChecker, get_current_user, get_job_service
from src.core.pagination import PaginatedResponse
from typing import Optional
import uuid

access_token_bearer = AccessTokenBearer()
job_application_router =  APIRouter()
role_checker_standard = Depends(RoleChecker(['ADMIN', 'USER', 'GUEST']))
role_checker_admin = Depends(RoleChecker(['ADMIN']))

@job_application_router.get(
    "/", 
    response_model=PaginatedResponse[JobApplication],
    dependencies=[role_checker_admin]
    )
async def get_all_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    session:AsyncSession = Depends(get_session), 
    token_details:dict=Depends(access_token_bearer),
    job_application_service:JobApplicationService=Depends(get_job_service),
    ):
    job_applications = await job_application_service.get_all_jobs(session,page,page_size,search,status)
    return job_applications

@job_application_router.get("/user", response_model=PaginatedResponse[JobApplication], dependencies=[role_checker_standard])
async def get_jobs_by_user_id(
    page: int = Query(1, ge=1), 
    page_size: int = Query(10, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
    session:AsyncSession = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    job_application_service:JobApplicationService=Depends(get_job_service)
    ):
    job_applications = await job_application_service.get_user_jobs(current_user.id,session,page,page_size,search,status)
    return job_applications

@job_application_router.get("/{id}", response_model=JobApplicationDetail, dependencies=[role_checker_standard])
async def get_job_by_id(
    id:str, 
    session:AsyncSession = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    job_application_service:JobApplicationService=Depends(get_job_service)
    ):
    job_application = await job_application_service.get_job( id, current_user.id, session)
    if job_application is not None :
        return job_application
    else :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

@job_application_router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobApplicationModel, response_model_exclude_none=True, dependencies=[role_checker_standard])
async def create_job_application(
    job_data:JobApplicationCreateModel, 
    session:AsyncSession = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    job_application_service:JobApplicationService=Depends(get_job_service)
    ) :
    job_application = await job_application_service.create_job(job_data,current_user.id, session)
    return job_application

@job_application_router.patch("/{id}", response_model_exclude_none=True, dependencies=[role_checker_standard])
async def update_job_application(
    id : str,job_data:JobApplicationUpdateModel,
    session:AsyncSession = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    job_application_service:JobApplicationService=Depends(get_job_service)
    ) :
    update_data = await job_application_service.update_job(id, current_user.id,job_data,session)
    
    if update_data:
        return update_data
    else :
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )
    
@job_application_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker_standard])
async def delete_job_application(
    id:str,session:AsyncSession = Depends(get_session), 
    current_user: User = Depends(get_current_user),
    job_application_service:JobApplicationService=Depends(get_job_service)
    ) :
    delete_data = await job_application_service.delete_job(id, current_user.id,session)
    if delete_data:
        return None
    else :
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        ) 