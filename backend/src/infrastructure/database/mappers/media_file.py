from src.domain.media_files.entities import MediaFile
from src.infrastructure.database.models import MediaFileModel, MediaFileModel

class MediaFileMapper:
	@staticmethod
	def to_domain(model: MediaFileModel) -> MediaFile:
		media_file = MediaFile(
			id=model.id,
			author_id=model.author_id,
			filename=model.filename,
			original_filename=model.original_filename,
			file_size=model.file_size,
			mime_type=model.mime_type,
			extension=model.extension,
			storage_path=model.storage_path,
			extra=model.extra,
			is_temp=model.is_temp,
			created_at=model.created_at,
			updated_at=model.updated_at,
		)
		return media_file

	@staticmethod
	def to_model(media_file: MediaFile) -> MediaFileModel:
		return MediaFileModel(
			id=media_file.id,
			author_id=media_file.author_id,
			filename=media_file.filename,
			original_filename=media_file.original_filename,
			file_size=media_file.file_size,
			mime_type=media_file.mime_type,
			extension=media_file.extension,
			storage_path=media_file.storage_path,
			extra=media_file.extra,
			is_temp=media_file.is_temp,
			created_at=media_file.created_at,
			updated_at=media_file.updated_at,
		)
