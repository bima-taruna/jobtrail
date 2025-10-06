from fastapi import FastAPI
from src.job_application.routes import job_application_router
from src.auth.routes import auth_router
from src.interview.routes import job_interview_router
from src.job_timeline.routes import job_timeline_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .middleware import register_middleware
@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"server is starting ... ")
    await init_db()
    yield
    print(f"server has been stopped ... ")
    
version = "v1"

app = FastAPI(
    title="Job Trail",
    version=version,
)

register_middleware(app)

app.include_router(job_application_router, prefix=f"/api/{version}/job_applications", tags=["job_applications"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(job_interview_router, prefix=f"/api/{version}", tags=["Job Interviews"])
app.include_router(job_timeline_router, prefix=f"/api/{version}", tags=["Job Timelines"])