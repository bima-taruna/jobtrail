from fastapi import APIRouter
from src.job_application.schemas import JobApplication, UpdateJobApplication
from fastapi.exceptions import HTTPException
from src.job_application.job_application_data import job_applications
job_application_router =  APIRouter()


@job_application_router.get("/", response_model=list[JobApplication])
def get_all_jobs():
    return job_applications


@job_application_router.get("/{id}")
def get_job_by_id(id:int):
    for job in job_applications:
        if job.id == id:
            return job
    raise HTTPException(
        status_code=404,
        detail="Job not found"
    )

@job_application_router.post("/")
def create_job_application(job_data:JobApplication) -> dict[str, list[JobApplication] | str | JobApplication] :
    job_data.id = len(job_applications) + 1
    job_applications.append(job_data)
    return {
        "message" : "200 item created succesfully",
        "item" : job_data,
        "result" : job_applications
    }

@job_application_router.patch("/{id}")
def update_job_application(id : int,job_data:UpdateJobApplication) :
    update_data = job_data.model_dump(exclude_unset=True)
    for job in job_applications:
        if job.id == id:
            for field, value in update_data.items():
                setattr(job, field, value)
            return job
    raise HTTPException(
        status_code=404,
        detail="Job not found"
    )
    
@job_application_router.delete("/{id}")
def delete_job_application(id:int) :
    for job in job_applications:
        if job.id == id:
            job_applications.remove(job)
            return {
                "message" : "selected item deleted"
            }
    raise HTTPException(
        status_code=404,
        detail="Job not found"
    ) 