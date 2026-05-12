from domain.interfaces.storage_service import StorageService
from src.application.media_files.queries import GetMediaFileQuery
from src.application.media_files.dtos import MediaFileDTO
from src.application.media_files.mappers import MediaFileMapper
from src.domain.media_files.exceptions import MediaFileNotFoundError
from src.infrastructure.database import UnitOfWork

class GetMediaFile:
	def __init__(self, uow: UnitOfWork, storage_service: StorageService):
		self.uow = uow
		self.storage_service = storage_service

	async def execute(self, query: GetMediaFileQuery) -> MediaFileDTO:
		async with self.uow:
			media_file = await self.uow.media_file.get(query.id)

			if not media_file:
				raise MediaFileNotFoundError.by_id(str(query.id))

			url = self.storage_service.get_url(media_file.storage_path)
			return MediaFileMapper.to_dto(media_file, url)
