from typing import List

from src.api.v1.messages.schemas import MessageTypeAPI
from src.application.sections.dtos import SectionDTO
from src.application.sections.queries import ListSectionsQuery
from . import schemas

class ListSectionsMapper:
	@staticmethod
	def to_query() -> ListSectionsQuery:
		return ListSectionsQuery()

	@staticmethod
	def to_response(dto_list: List[SectionDTO]) -> List[schemas.SectionResponse]:
		return [
			schemas.SectionResponse(
				id=dto.id,
				code=dto.code,
				message_types=[
					schemas.SectionMessageTypeResponse(
						section_id=i.section_id,
						message_type=MessageTypeAPI(i.message_type.value),
						allow_comments=i.allow_comments
					)
					for i in dto.message_types
				]
			)
			for dto in dto_list
		]
