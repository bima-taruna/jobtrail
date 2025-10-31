from fastapi import APIRouter, status, Depends, Body
from src.auth.dependencies import RoleChecker, get_current_user, get_timeline_service
from src.db.models import JobTimeline, User
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .services import JobTimelineService
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from src.job_timeline.schemas import JobTimelineCreateModel, JobTimelineUpdateModel
from typing import Annotated
import uuid

job_timeline_router = APIRouter(
    prefix="/job-applications/{job_application_id}/job-timelines",
    tags=["Job Timelines"],
)

role_checker_standard = Depends(RoleChecker(["ADMIN", "USER", "GUEST"]))
Session = Annotated[AsyncSession, Depends(get_session)]
JobTimelineServices = Annotated[JobTimelineService, Depends(get_timeline_service)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@job_timeline_router.get(
    "/", response_model=list[JobTimeline], dependencies=[role_checker_standard]
)
async def get_all_job_timelines(
    job_application_id: str,
    session: Session,
    job_timeline_services: JobTimelineServices,
    current_user: CurrentUser,
):
    job_timelines = await job_timeline_services.get_all_timelines_by_app_id(
        job_application_id, current_user.id, session
    )
    return job_timelines


@job_timeline_router.get(
    "/{job_timeline_id}",
    response_model=JobTimeline,
    dependencies=[role_checker_standard],
)
async def get_job_timeline_by_id(
    job_application_id: str,
    job_timeline_id: str,
    session: Session,
    job_timeline_services: JobTimelineServices,
    current_user: CurrentUser,
):
    job_timeline = job_timeline_services.get_timelines_by_id(
        job_application_id, job_timeline_id, current_user.id, session
    )
    if job_timeline is not None:
        return job_timeline
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="timeline not found"
        )


@job_timeline_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=JobTimeline,
    response_model_exclude_none=True,
    dependencies=[role_checker_standard],
)
async def create_job_application(
    job_application_id: uuid.UUID,
    timeline_data: JobTimelineCreateModel,
    session: Session,
    job_timeline_services: JobTimelineServices,
    current_user: CurrentUser,
):
    job_timeline = await job_timeline_services.create_job_timeline(
        timeline_data, job_application_id, current_user.id, session
    )
    return job_timeline


@job_timeline_router.delete(
    "/undo",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker_standard],
)
async def undo_job_timeline(
    job_application_id: str,
    session: Session,
    job_timeline_services: JobTimelineServices,
    current_user: CurrentUser,
):
    delete_data = await job_timeline_services.undo_job_timeline(
        job_application_id, current_user.id, session
    )
    if delete_data:
        return JSONResponse(
            content={
                "message": "Success Undo",
            }
        )
    else:
        raise HTTPException(status_code=404, detail="timeline not found")


@job_timeline_router.delete(
    "/reset",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker_standard],
)
async def reset_job_timeline(
    job_application_id: str,
    session: Session,
    job_timeline_services: JobTimelineServices,
    current_user: CurrentUser,
):
    delete_data = await job_timeline_services.reset_job_timeline(
        job_application_id, current_user.id, session
    )
    if delete_data:
        return JSONResponse(
            content={
                "message": "Success Reset the timeline",
            }
        )
    else:
        raise HTTPException(status_code=404, detail="timeline not found")


@job_timeline_router.patch(
    "/{timeline_id}",
    response_model_exclude_none=True,
    dependencies=[role_checker_standard],
)
async def update_job_application(
    job_application_id: str,
    job_timeline_id: str,
    update_data: JobTimelineUpdateModel,
    session: Session,
    job_timeline_services: JobTimelineServices,
    current_user: CurrentUser,
):
    update_timeline_data = await job_timeline_services.update_job_timeline(
        job_application_id, job_timeline_id, current_user.id, update_data, session
    )

    if update_timeline_data:
        return update_data
    else:
        raise HTTPException(status_code=404, detail="timeline not found")


@job_timeline_router.delete(
    "/{timeline_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[role_checker_standard],
)
async def delete_job_application(
    job_application_id: str,
    timeline_id: str,
    session: Session,
    job_timeline_services: JobTimelineServices,
    current_user: CurrentUser,
):
    delete_data = await job_timeline_services.delete_job_timeline(
        job_application_id, timeline_id, current_user.id, session
    )
    if delete_data:
        return None
    else:
        raise HTTPException(status_code=404, detail="timeline not found")


@job_timeline_router.patch(
    "/{timeline_id}/note",
    response_model_exclude_none=True,
    dependencies=[role_checker_standard],
)
async def update_timeline_note(
    job_application_id: str,
    timeline_id: str,
    session: Session,
    job_timeline_services: JobTimelineServices,
    current_user: CurrentUser,
    note_update: str = Body(...),
):
    update_note_data = await job_timeline_services.update_timeline_note(
        job_application_id, timeline_id, current_user.id, note_update, session
    )

    if update_note_data:
        return update_note_data
    else:
        raise HTTPException(status_code=404, detail="timeline not found")
