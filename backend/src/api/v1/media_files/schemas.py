from pydantic import BaseModel

class MediaFileResponse(BaseModel):
	original_filename: str
	file_size: int
	mime_type: str
	extension: str
	url: str
