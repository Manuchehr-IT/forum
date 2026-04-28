from src.domain.sections.entities import Section
from .dtos import SectionDTO, SectionMessageTypeDTO

class SectionMapper:
	@staticmethod
	def to_dto(section: Section) -> SectionDTO:
		return SectionDTO(
			id=section.id,
			code=section.code,
			openai_prompt=section.openai_prompt,
			tech_version=section.tech_version,
			enable_openai=section.enable_openai,
			allow_hide=section.allow_hide,
			created_at=section.created_at,
			updated_at=section.updated_at,
			message_types=[
				SectionMessageTypeDTO(
					section_id=section.id,
					message_type=i.message_type,
					allow_comments=i.allow_comments
				)
				for i in section.allowed_message_types
			]
		)
