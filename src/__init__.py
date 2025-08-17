from fastapi import FastAPI
from src.job_application.routes import job_application_router

version = "v1"

app = FastAPI(
    title="Job Trail",
    version=version
)

app.include_router(job_application_router, prefix=f"/api/{version}/job_applications", tags=["job_applications"])