import shutil
import uuid
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cellmetpro_server.config import get_settings
from cellmetpro_server.database import get_session
from cellmetpro_server.models import File, FileStatus, FileType, Project
from cellmetpro_server.schemas import (
    FileRegister,
    FileResponse,
    FileUpdate,
)
from cellmetpro_server.utils.const import ErrCode

router = APIRouter(prefix="/projects", tags=["Files", "Projects"])

ALLOWED_EXTENSIONS = {".h5ad", ".csv", ".mtx"}

Session = Annotated[AsyncSession, Depends(get_session)]


@router.post("/{project_id}/files/register", response_model=FileResponse)
async def register_file(project_id: str, body: FileRegister, session: Session) -> File:
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.FILE_NOT_FOUND,
        )
    elif project.deleted_at is not None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.PROJECT_NOT_FOUND,
        )

    resolved = Path(body.path).resolve()
    if not resolved.exists() or not resolved.is_file():
        raise HTTPException(
            status_code=400,
            detail=ErrCode.FILE_PATH_INCORRECT,
        )
    elif resolved.suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=422, detail=ErrCode.FILE_EXT_NOT_ALLOWED)

    file = File(
        id=str(uuid.uuid4()),
        project_id=project_id,
        filename=resolved.name,
        size_bytes=resolved.stat().st_size,
        path=str(resolved),
        status=FileStatus.AVAILABLE.value,
        job_id=None,
        file_type=body.file_type,
    )
    session.add(file)
    await session.commit()
    await session.refresh(file)

    return file


@router.post("/{project_id}/files", response_model=FileResponse)
async def upload_file(
    project_id: str,
    file: UploadFile,
    session: Session,
    file_type: str = Form(default=FileType.UNSPECIFIED.value),
) -> File:
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.FILE_NOT_FOUND,
        )
    elif project.deleted_at is not None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.PROJECT_NOT_FOUND,
        )

    # validation
    file_extension = Path(file.filename or "").suffix
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=422,
            detail=ErrCode.FILE_EXT_NOT_ALLOWED,
        )

    # define file path
    file_id = str(uuid.uuid4())
    dest = (
        Path(get_settings().upload_dir) / project_id / file_id / (file.filename or "")
    )
    dest.parent.mkdir(parents=True, exist_ok=True)
    # write chunks
    with open(dest, "wb") as f:
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            f.write(chunk)

    row = File(
        id=file_id,
        filename=file.filename or "",
        size_bytes=dest.stat().st_size,
        project_id=project_id,
        status=FileStatus.AVAILABLE.value,
        path=str(dest),
        file_type=file_type,
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)

    return row


@router.get("/{project_id}/files", response_model=list[FileResponse])
async def list_files(project_id: str, session: Session) -> list[File]:
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.PROJECT_NOT_FOUND,
        )

    files = await session.scalars(select(File).where(File.project_id == project_id))
    return list(files.all())


@router.get("/{project_id}/files/{file_id}", response_model=FileResponse)
async def get_file(project_id: str, file_id: str, session: Session) -> File:
    file = await session.get(File, file_id)
    if file is None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.FILE_NOT_FOUND,
        )
    elif file.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.FILE_NOT_LINKED_TO_PROJECT,
        )

    return file


@router.delete("/{project_id}/files/{file_id}", status_code=204)
async def delete_file(project_id: str, file_id: str, session: Session) -> None:
    file = await session.get(File, file_id)
    if file is None:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.FILE_NOT_FOUND,
        )
    elif file.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.FILE_NOT_LINKED_TO_PROJECT,
        )

    file_path = Path(file.path)
    upload_root = Path(get_settings().upload_dir)
    # Registered files: only remove the DB row
    # Uploaded copies: we own them, clean up the whole file_id directory
    if file_path.is_relative_to(upload_root):
        shutil.rmtree(file_path.parent, ignore_errors=True)

    await session.delete(file)
    await session.commit()


@router.patch("/{project_id}/files/{file_id}", response_model=FileResponse)
async def update_file(
    project_id: str, file_id: str, body: FileUpdate, session: Session
) -> File:
    file = await session.get(File, file_id)
    if file is None:
        raise HTTPException(status_code=404, detail=ErrCode.FILE_NOT_FOUND)
    elif file.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail=ErrCode.FILE_NOT_LINKED_TO_PROJECT,
        )

    if body.file_type is not None:
        file.file_type = body.file_type

    if body.filename is not None:
        new_name = Path(body.filename).name

        file_path = Path(file.path)
        if file_path.exists():
            new_path = file_path.parent / new_name
            # avoid renaming if filename alread present in path
            # there is a risk of silent overwrite on most systems
            if new_path.exists():
                raise HTTPException(status_code=409, detail=ErrCode.FILE_NAME_TAKEN)

            file_path.rename(new_path)
            file.path = str(new_path)

            file.filename = new_name

    await session.commit()
    await session.refresh(file)

    return file
