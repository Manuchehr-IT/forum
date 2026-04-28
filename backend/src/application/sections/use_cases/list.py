from typing import List

from src.application.sections.queries import ListSectionsQuery
from src.application.sections.dtos import SectionDTO
from src.application.sections.mappers import SectionMapper
from src.infrastructure.database import UnitOfWork

class ListSections:
	def __init__(self, uow: UnitOfWork):
		self.uow = uow

	async def execute(self, query: ListSectionsQuery) -> List[SectionDTO]:
		async with self.uow:
			sections = await self.uow.section.list()
			return [SectionMapper.to_dto(section) for section in sections]
