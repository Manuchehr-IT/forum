from datetime import datetime
from typing import List, Tuple
from uuid import UUID, uuid4

from src.domain.themes.value_objects import ThemeSection

class Theme:
	def __init__(
		self,
		id: UUID,
		parent_id: UUID | None,
		author_id: UUID,
		title: str,
		is_group: bool = False,
		created_at: datetime | None = None,
		updated_at: datetime | None = None,
		sections: List[ThemeSection] | None = None,
	):
		self.id = id
		self.parent_id = parent_id
		self.author_id = author_id
		self.title = title
		self.is_group = is_group
		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or self.created_at

		self._sections = sections or []

	@property
	def sections(self) -> Tuple[ThemeSection, ...]:
		return tuple(self._sections)

	def _touch(self):
		self.updated_at = datetime.utcnow()

	def has_section(self, section_id: UUID) -> bool:
		return any(section_id == ts.section_id for ts in self._sections)

	def add_section(self, section_id: UUID, section_code: str, is_visible: bool = True):
		if self.has_section(section_id):
			raise ValueError(f"Section {section_id} already in theme")

		theme_section = ThemeSection(section_id=section_id, section_code=section_code, is_visible=is_visible)
		self._sections.append(theme_section)

		self._touch()

	# def update_section(self, section_id: UUID, section_code: str, is_visible: bool = True):
	# 	if not self.has_section(section_id):
	# 		raise ValueError(f"Section {section_id} not found in theme")

	def update_section(self, section_id: UUID, section_code: str, is_visible: bool = True) -> None:
		"""Обновляет настройки существующей секции темы"""
		for ts in self._sections:
			if ts.section_id == section_id:
				if ts.section_code != section_code:
					ts.section_code = section_code
					self._touch()
				if ts.is_visible != is_visible:
					ts.is_visible = is_visible
					self._touch()
				return

	@classmethod
	def create(cls, author_id: UUID, title: str, parent_id: UUID | None = None, is_group: bool = False):
		return cls(
			id=uuid4(),
			parent_id=parent_id,
			author_id=author_id,
			title=title,
			is_group=is_group
		)

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			id=record["id"],
			parent_id=record["parent_id"],
			author_id=record["author_id"],
			title=record["title"],
			is_group=record["is_group"],
			created_at=record["created_at"],
			updated_at=record["updated_at"],
		)

	@classmethod
	def from_db_with_sections(cls, theme_record: dict, section_records: List[dict]):
		theme = cls.from_db_record(theme_record)
		theme._sections = [ThemeSection.from_db_record(section) for section in section_records]
		return theme
