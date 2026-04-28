from asyncpg import Pool
from fastapi import Depends
from uuid import UUID

from src.api.dependencies import get_uow, get_db_pool
from src.api.v1.users.dependencies import get_current_user
from src.application.sections.dtos import SectionDTO
from src.application.sections.queries import GetSectionQuery
from src.application.sections.use_cases import GetSection, ListSections
from src.application.users.dtos import UserDTO
from src.domain.sections.repository import SectionRepository
from src.infrastructure.database.repositories.raw_sql.sections import RawSQLSectionRepository
from src.infrastructure.database.uow import UnitOfWork

async def get_section_repository(
	pool: Pool = Depends(get_db_pool)
) -> SectionRepository:
	return RawSQLSectionRepository(pool)

async def get_retrieve_section(
	section_repo: SectionRepository = Depends(get_section_repository)
) -> GetSection:
	return GetSection(section_repo)

async def get_section(
	section_id: UUID,
	user: UserDTO = Depends(get_current_user),
	get_section: GetSection = Depends(get_retrieve_section)
) -> SectionDTO:
	command = GetSectionQuery.by_id(section_id)
	return await get_section.execute(command)

async def provide_list_sections(uow: UnitOfWork = Depends(get_uow)):
	return ListSections(uow)
