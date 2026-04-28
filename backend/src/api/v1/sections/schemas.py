from pydantic import BaseModel
from typing import List
from uuid import UUID

from src.api.v1.messages.schemas import MessageTypeAPI

class SectionMessageTypeResponse(BaseModel):
	section_id: UUID
	message_type: MessageTypeAPI
	allow_comments: bool

class SectionResponse(BaseModel):
	id: UUID
	code: str
	message_types: List[SectionMessageTypeResponse]
