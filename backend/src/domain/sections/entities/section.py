from datetime import datetime
from typing import List, Tuple
from uuid import UUID, uuid4

from src.domain.messages.value_objects import MessageType
from src.domain.sections.exceptions import CannotCommentOnCommentError, SectionMessageTypeConflictError, SectionValidationError, SectionAIDisabled
from src.domain.sections.value_objects import TechVersionType, SectionMessageType

class Section:
	def __init__(
		self,
		id: UUID,
		parent_id: UUID | None,
		code: str,
		openai_prompt: str | None,
		tech_version: TechVersionType,
		enable_openai: bool = True,
		allow_hide: bool = True,
		created_at: datetime | None = None,
		updated_at: datetime | None = None,
		allowed_message_types: List[SectionMessageType] | None = None
	):
		self.id = id
		self.parent_id = parent_id
		self.code = code
		self.openai_prompt = openai_prompt
		self.tech_version = tech_version
		self.enable_openai = enable_openai
		self.allow_hide = allow_hide

		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or self.created_at

		self._allowed_message_types = allowed_message_types or []

	@property
	def allowed_message_types(self) -> Tuple[SectionMessageType, ...]:
		return tuple(self._allowed_message_types)

	def _touch(self):
		self.updated_at = datetime.utcnow()

	def has_allowed_message_type(self, message_type: MessageType) -> bool:
		return any(message_type == amt.message_type for amt in self._allowed_message_types)

	def has_allowed_comment_for_message_type(self, message_type: MessageType) -> bool:
		return any(message_type == amt.message_type for amt in self._allowed_message_types if amt.allow_comments is True)

	def ensure_allowed_message_type(self, message_type: MessageType):
		if not self.has_allowed_message_type(message_type):
			raise SectionValidationError.message_type_not_allowed(message_type, self.code, self.allowed_message_types)

	def ensure_allowed_comment_for_message_type(self, message_type: MessageType):
		if message_type == MessageType.COMMENT:
			raise CannotCommentOnCommentError(f"Cannot comment on {message_type.value}")

		if not self.has_allowed_comment_for_message_type(message_type):
			raise SectionValidationError.comments_not_allowed(message_type, self.code, self.allowed_message_types)

	def can_use_ai(self) -> bool:
		return bool(self.enable_openai and self.openai_prompt)

	def ensure_ai_available(self):
		if not self.can_use_ai():
			raise SectionAIDisabled(self.id, self.code)

	def add_allowed_message_type(self, message_type: MessageType, allow_comments: bool) -> None:
		if self.has_allowed_message_type(message_type):
			raise SectionMessageTypeConflictError(message_type)

		section_message_type = SectionMessageType(message_type=message_type, allow_comments=allow_comments)
		self._allowed_message_types.append(section_message_type)

		self._touch()

	def update_allowed_message_type(self, message_type: MessageType, allow_comments: bool) -> None:
		"""Обновляет настройки существующего типа сообщения"""
		for mt in self._allowed_message_types:
			if mt.message_type == message_type:
				if mt.allow_comments != allow_comments:
					mt.allow_comments = allow_comments
					self._touch()
				return

		# raise SectionMessageTypeNotFoundError(f"Message type {message_type} not found")

	def remove_allowed_message_type(self, message_type: MessageType) -> None:
		self._allowed_message_types = [mt for mt in self._allowed_message_types if mt.message_type != message_type]

		self._touch()

	def change_parent(self, new_parent_id: UUID | None):
		"""Изменить родителя секции"""
		if self.id == new_parent_id:
			return
			# raise DomainError("Секция не может быть своим родителем")
		self.parent_id = new_parent_id

		self._touch()

	@classmethod
	def create(cls, code: str, allow_hide: bool, tech_version: TechVersionType, parent_id: UUID | None = None, openai_prompt: str | None = None):
		return cls(
			id=uuid4(),
			parent_id=parent_id,
			code=code,
			allow_hide=allow_hide,
			tech_version=tech_version,
			openai_prompt=openai_prompt,
		)

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			id=record["id"],
			parent_id=record["parent_id"],
			code=record["code"],
			openai_prompt=record["openai_prompt"],
			tech_version=TechVersionType(record["tech_version"]),
			enable_openai=record["enable_openai"],
			allow_hide=record["allow_hide"],
			created_at=record["created_at"],
			updated_at=record["updated_at"],
		)

	@classmethod
	def from_db_with_allowed_message_types(cls, section_record: dict, section_message_type_records: List[dict]):
		section = cls.from_db_record(section_record)
		section._allowed_message_types = [SectionMessageType.from_db_record(record) for record in section_message_type_records]
		return section
