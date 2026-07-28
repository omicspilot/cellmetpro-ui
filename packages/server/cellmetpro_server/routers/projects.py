from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cellmetpro_server.database import get_session
from cellmetpro_server.models import Project
from cellmetpro_server.schemas import ProjectCreate, ProjectResponse
from cellmetpro_server.utils.const import ErrCode

router = APIRouter(prefix="/projects", tags=["Projects"])

Session = Annotated[AsyncSession, Depends(get_session)]


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(body: ProjectCreate, session: Session) -> Project:
    project = Project(
        id=str(uuid4()),
        name=body.name,
        description=body.description,
        workspace_path=body.workspace_path,
    )
    session.add(project)
    await session.commit()

    await session.refresh(project)
    return project


@router.get("/", response_model=list[ProjectResponse])
async def list_projects(session: Session) -> list[Project]:
    projects = await session.scalars(
        select(Project).where(Project.deleted_at.is_(None))
    )
    return list(projects.all())


@router.get("/trash", response_model=list[ProjectResponse])
async def list_trash(session: Session) -> list[Project]:
    projects = await session.scalars(
        select(Project).where(Project.deleted_at.is_not(None))
    )
    return list(projects.all())


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, session: Session) -> Project:
    project = await session.get(Project, project_id)

    if project is None or project.deleted_at is not None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.PROJECT_NOT_FOUND,
        )

    return project


# Soft delete projects. Hide from list of active projects
# But still visible in the trash section
@router.delete("/{project_id}", status_code=204)
async def soft_delete_project(project_id: str, session: Session) -> None:
    project = await session.get(Project, project_id)

    if project is None or project.deleted_at is not None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.PROJECT_NOT_FOUND,
        )

    project.deleted_at = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(project)


@router.delete("/{project_id}/permanent", status_code=204)
async def hard_delete_project(project_id: str, session: Session) -> None:
    project = await session.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.PROJECT_NOT_FOUND,
        )

    await session.delete(project)
    await session.commit()


@router.patch("/{project_id}/restore", response_model=ProjectResponse)
async def restore_project(project_id: str, session: Session) -> Project:
    project = await session.get(Project, project_id)

    if project is None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.PROJECT_NOT_FOUND,
        )
    elif project.deleted_at is None:
        raise HTTPException(status_code=400, detail=ErrCode.PROJECT_NOT_DELETED)

    project.deleted_at = None

    await session.commit()
    await session.refresh(project)

    return project
