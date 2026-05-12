from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import Self

from src.infrastructure.database.repositories import SectionRepository, MediaFileRepository

class UnitOfWork:
	def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
		self._session_factory = session_factory
		self._session: AsyncSession | None = None

	async def __aenter__(self) -> Self:
		if self._session is not None:
			raise RuntimeError("Unit of Work already started")

		self._session = self._session_factory()
		await self._session.begin()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		if not self._session:
			return

		try:
			if exc_type:
				await self._session.rollback()
			else:
				await self._session.commit()
		finally:
			await self._session.close()
			self._session = None

	@property
	def session(self) -> AsyncSession:
		if self._session is None:
			raise RuntimeError("Unit of Work not started")
		return self._session

	@property
	def section(self) -> SectionRepository:
		return SectionRepository(self.session)

	@property
	def media_file(self) -> MediaFileRepository:
		return MediaFileRepository(self.session)
