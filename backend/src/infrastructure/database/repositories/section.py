from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from src.domain.sections.entities import Section
from src.infrastructure.database.mappers.section import SectionMapper
from src.infrastructure.database.models import SectionModel

class SectionRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get(self, id: UUID) -> Section | None:
		model = await self.session.get(SectionModel, id)
		if model:
			return SectionMapper.to_domain(model)

	async def get_by_code(self, code: str) -> Section | None:
		result = await self.session.execute(select(SectionModel).where(SectionModel.code == code))
		model = result.scalar_one_or_none()
		if model:
			return SectionMapper.to_domain(model)

	async def list(self) -> List[Section]:
		result = await self.session.execute(select(SectionModel))
		return [SectionMapper.to_domain(model) for model in result.scalars().all()]
