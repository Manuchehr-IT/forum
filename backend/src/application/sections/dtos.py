from datetime import datetime
from pydantic import BaseModel
from typing import List
from uuid import UUID

from src.domain.messages.value_objects.message import MessageType
from src.domain.sections.value_objects import TechVersionType

class SectionMessageTypeDTO(BaseModel):
	section_id: UUID
	message_type: MessageType
	allow_comments: bool

class SectionDTO(BaseModel):
	id: UUID
	code: str
	openai_prompt: str | None
	tech_version: TechVersionType
	enable_openai: bool
	allow_hide: bool

	created_at: datetime
	updated_at: datetime
	message_types: List[SectionMessageTypeDTO]
