import shutil
import tempfile
import uuid
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter(prefix="/files", tags=["Files"])

ALLOWED_FILES_UPLOAD = {".h5ad", ".csv", ".mtx"}


class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    size_bytes: int


class FileMetadataResponse(BaseModel):
    file_id: str
    filename: str
    size_bytes: int


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile) -> FileUploadResponse:
    # validation
    file_extension = Path(file.filename or "").suffix
    if file_extension not in ALLOWED_FILES_UPLOAD:
        raise HTTPException(status_code=422, detail="Unsupported file type")

    # define file path
    file_id = str(uuid.uuid4())
    filename = file.filename or ""
    file_path = Path(tempfile.gettempdir()) / "cellmetpro" / file_id / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    # write chunks
    with open(file_path, "wb") as dest:
        while chunk := await file.read(1024 * 1024):  # 1MB chunks
            dest.write(chunk)

    return FileUploadResponse(
        file_id=file_id,
        filename=file.filename or "",
        size_bytes=file_path.stat().st_size,
    )


@router.get("/{file_id}", response_model=FileMetadataResponse)
async def get_file(file_id: str) -> FileMetadataResponse:
    # check file exists
    dir_path = Path(tempfile.gettempdir()) / "cellmetpro" / file_id
    if not dir_path.exists():
        raise HTTPException(404)

    # get file inside path
    file = next(dir_path.iterdir())

    return FileMetadataResponse(
        file_id=file_id, filename=file.name, size_bytes=file.stat().st_size
    )


@router.delete("/{file_id}", status_code=204)
async def delete_file(file_id: str) -> None:
    # check file exists
    dir_path = Path(tempfile.gettempdir()) / "cellmetpro" / file_id
    if not dir_path.exists():
        raise HTTPException(404)

    shutil.rmtree(dir_path)
