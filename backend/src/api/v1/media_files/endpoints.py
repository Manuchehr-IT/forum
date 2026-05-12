from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from typing import List
from uuid import UUID

from src.api.v1.users.dependencies import get_current_user
from src.application.media_files.commands import UploadFilesCommand
from src.application.media_files.queries import GetMediaFileQuery
from src.application.media_files.use_cases.get import GetMediaFile
from src.application.media_files.use_cases.upload_files import UploadFiles
from src.application.users.dtos import UserDTO
from .dependencies import get_upload_files, provide_get_media_file
from . import schemas

router = APIRouter(prefix="/media_files", tags=["MediaFiles"])

@router.post("/uploads", response_model=List[UUID], summary="Upload media files", description="<b>Загрузка медифайлов в временное хранилище.</b>")
async def uploads_endpoint(
	files: List[UploadFile],
	user: UserDTO = Depends(get_current_user),
	upload_files: UploadFiles = Depends(get_upload_files)
):
	command = UploadFilesCommand(author_id=user.id, files=files)
	media_file_ids = await upload_files.execute(command)
	return media_file_ids

@router.get("/{id}", response_model=schemas.MediaFileResponse)
async def get_file_endpoints(
	id: UUID,
	user: UserDTO = Depends(get_current_user),
	get_media_file: GetMediaFile = Depends(provide_get_media_file)
):
	query = GetMediaFileQuery(id=id)
	media_file_dto = await get_media_file.execute(query)
	return schemas.MediaFileResponse(
		original_filename=media_file_dto.original_filename,
		file_size=media_file_dto.file_size,
		mime_type=media_file_dto.mime_type,
		extension=media_file_dto.extension,
		url=media_file_dto.url,
	)

@router.get("/test/{path:path}")
async def test_get_file_endpoints(path: str):
	return FileResponse(path)
