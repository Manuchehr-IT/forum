from typing import Any
from uuid import UUID

class MessageMediaFile:
	def __init__(
		self,
		media_file_id: UUID,
		sort_order: int,
		original_filename: str | None = None,
		file_size: int | None = None,
		mime_type: str | None = None,
		extension: str | None = None,
		storage_path: str | None = None,
	):
		self.media_file_id = media_file_id
		self.sort_order = sort_order
		self.original_filename = original_filename
		self.file_size = file_size
		self.mime_type = mime_type
		self.extension = extension
		self.storage_path = storage_path

	def to_dict(self) -> dict:
		return {
			"media_file_id": self.media_file_id,
			"sort_order": self.sort_order
		}

	@classmethod
	def from_db_record(cls, record: dict[str, Any]):
		return cls(
			media_file_id=record["media_file_id"],
			sort_order=record["sort_order"],
			original_filename=record.get("original_filename"),
			file_size=record.get("file_size"),
			mime_type=record.get("mime_type"),
			extension=record.get("extension"),
			storage_path=record.get("storage_path"),
		)
