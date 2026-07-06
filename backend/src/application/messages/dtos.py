from datetime import datetime
from pydantic import BaseModel, Field
from typing import TYPE_CHECKING, List
from uuid import UUID

from src.domain.messages.value_objects import MessageType, TaskAssignmentStatus

if TYPE_CHECKING:
	from src.domain.messages.value_objects.message_media_file import MessageMediaFile

class MessageMediaFileDTO(BaseModel):
	media_file_id: UUID
	sort_order: int
	original_filename: str | None = None
	file_size: int | None = None
	mime_type: str | None = None
	extension: str | None = None
	url: str = ""

	@classmethod
	def from_domain(cls, mf: "MessageMediaFile") -> "MessageMediaFileDTO":
		return cls(
			media_file_id=mf.media_file_id,
			sort_order=mf.sort_order,
			original_filename=mf.original_filename,
			file_size=mf.file_size,
			mime_type=mf.mime_type,
			extension=mf.extension,
			url=f"/api/v1/media_files/{mf.media_file_id}",
		)

class MessageDTO(BaseModel):
	"""DTO для передачи данных агрегата Message между слоями"""
	id: UUID
	author_id: UUID
	theme_id: UUID
	section_id: UUID
	type: MessageType
	text: str | None
	is_openai_generated: bool
	created_at: datetime
	updated_at: datetime

	# Для TASK:
	ratio: int | None = None

	# Для TASK_ASSIGNMENT:
	content_id: UUID | None = None # Также для Comment
	is_partially: bool | None = None
	status: TaskAssignmentStatus | None = None
	expires_at: datetime | None = None

	# Для COMMENT:
	reply_to_message_id: UUID | None = None

	media_files: List[MessageMediaFileDTO] = Field(default_factory=list)

class MessageImproveTextDTO(BaseModel):
	input_text: str
	output_text: str | None
