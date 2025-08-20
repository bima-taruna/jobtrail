from fastapi import FastAPI
from src.job_application.routes import job_application_router
from contextlib import asynccontextmanager
from src.db.main import init_db
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
    lifespan=life_span
)

app.include_router(job_application_router, prefix=f"/api/{version}/job_applications", tags=["job_applications"])