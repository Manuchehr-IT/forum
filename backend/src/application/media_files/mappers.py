from .dtos import MediaFileDTO
from src.domain.media_files.entities import MediaFile

class MediaFileMapper:
	@staticmethod
	def to_dto(media_file: MediaFile, url: str) -> MediaFileDTO:
		return MediaFileDTO(
			id=media_file.id,
			author_id=media_file.author_id,
			filename=media_file.filename,
			original_filename=media_file.original_filename,
			file_size=media_file.file_size,
			mime_type=media_file.mime_type,
			extension=media_file.extension,
			is_temp=media_file.is_temp,
			created_at=media_file.created_at,
			updated_at=media_file.updated_at,

			url=url
		)
