from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.domain.media_files.entities import MediaFile
from src.infrastructure.database.mappers.media_file import MediaFileMapper
from src.infrastructure.database.models import MediaFileModel

class MediaFileRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get(self, id: UUID) -> MediaFile | None:
		model = await self.session.get(MediaFileModel, id)
		if model:
			return MediaFileMapper.to_domain(model)

	# async def list_by_ids(self, ids: List[UUID]) -> List[MediaFile]:
	# 	if not ids:
	# 		return []

	# 	result = await self.session.execute(select(MediaFileModel).where(MediaFileModel.id.in_(ids)))
	# 	return [MediaFileMapper.to_domain(model) for model in result.scalars().all()]
