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
		section._allowed_message_types.extend([SectionMessageTypeMapper.to_domain(i) for i in model.allowed_message_types])
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
			allowed_message_types=[SectionMessageTypeMapper.to_model(i) for i in section.allowed_message_types]
		)

class SectionMessageTypeMapper:
	@staticmethod
	def to_domain(model: SectionMessageTypeModel):
		return SectionMessageType(
			# id=model.id, TODO
			message_type=MessageType(model.message_type),
			allow_comments=model.allow_comments
		)

	@staticmethod
	def to_model(message_type: SectionMessageType):
		return SectionMessageTypeModel(
			# id=message_type.id, TODO
			message_type=message_type.message_type.value,
			allow_comments=message_type.allow_comments
		)
