from src.domain.messages.value_objects import MessageType
from src.domain.sections.entities import Section
from src.domain.sections.value_objects import SectionMessageType, TechVersionType
from src.infrastructure.database.models import SectionModel, SectionMessageTypeModel

class SectionMapper:
	@staticmethod
	def to_domain(model: SectionModel) -> Section:
		section = Section(
			id=model.id,
			parent_id=model.parent_id,
			code=model.code,
			openai_prompt=model.openai_prompt,
			tech_version=TechVersionType(model.tech_version),
			enable_openai=model.enable_openai,
			allow_hide=model.allow_hide,
			created_at=model.created_at,
			updated_at=model.updated_at,
		)
		section._allowed_message_types = [
			SectionMessageType(
				message_type=MessageType(i.message_type),
				allow_comments=i.allow_comments
			)
			for i in model.allowed_message_types
		]
		return section

	@staticmethod
	def to_model(section: Section) -> SectionModel:
		return SectionModel(
			id=section.id,
			parent_id=section.parent_id,
			code=section.code,
			openai_prompt=section.openai_prompt,
			tech_version=section.tech_version.value,
			enable_openai=section.enable_openai,
			allow_hide=section.allow_hide,
			created_at=section.created_at,
			updated_at=section.updated_at,
			allowed_message_types=[
				SectionMessageTypeModel(
					message_type=i.message_type.value,
					allow_comments=i.allow_comments
				)
				for i in section.allowed_message_types
			]
		)
