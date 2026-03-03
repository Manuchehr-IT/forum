from typing import Any, Dict, List
from uuid import UUID

from src.domain.messages.value_objects import MessageType
from src.domain.sections.entities import Section
from src.domain.sections.exceptions import SectionNotFoundError
from src.domain.sections.repository import SectionRepository
from src.domain.sections.value_objects import TechVersionType

SECTIONS = [
	{
		"code": "discussion",
		"tech_version": TechVersionType.MINIMUM,
		"message_types": [
			{"message_type": MessageType.POST, "allow_comments": False}
		]
	},
	{
		"code": "experience_exchange",
		"tech_version": TechVersionType.MINIMUM,
		"message_types": [
			{"message_type": MessageType.POST}
		]
	},
	{
		"code": "description",
		"allow_hide": False,
		"tech_version": TechVersionType.MINIMUM,
		"message_types": [
			{"message_type": MessageType.POST}
		]
	},
	{
		"code": "perfect_result",
		"tech_version": TechVersionType.MINIMUM,
		"children": [
			{
				"code": "desirable_effects",
				"tech_version": TechVersionType.MINIMUM,
				"message_types": [
					{"message_type": MessageType.POST}
				]
			},
			{
				"code": "technical_modeling",
				"tech_version": TechVersionType.MINIMUM,
				"message_types": [
					{"message_type": MessageType.POST}
				]
			},
			{
				"code": "undesirable_effects",
				"tech_version": TechVersionType.MINIMUM,
				"message_types": [
					{"message_type": MessageType.POST}
				]
			}
		],
	},
	{
		"code": "project_modules",
		"tech_version": TechVersionType.MINIMUM,
	},
	{
		"code": "chat_ideas",
		"tech_version": TechVersionType.FULL,
		"openai_prompt": "Улучшите текст идеи, сделав его максимально лаконичным. Ответь только улучшенным текстом, без дополнительных комментариев.",
		"message_types": [
			{"message_type": MessageType.POST}
		]
	},
	{
		"code": "chat_qa",
		"tech_version": TechVersionType.FULL,
		"message_types": [
			{"message_type": MessageType.POST}
		]
	},
	{
		"code": "chat_publications",
		"tech_version": TechVersionType.FULL,
		"message_types": [
			{"message_type": MessageType.POST}
		]
	},
	{
		"code": "chat_tasks",
		"tech_version": TechVersionType.FULL,
		"message_types": [
			{"message_type": MessageType.TASK},
			{"message_type": MessageType.TASK_ASSIGNMENT, "allow_comments": False}
		]
	},
	{
		"code": "chat_experiments",
		"tech_version": TechVersionType.FULL,
		"message_types": [
			{"message_type": MessageType.TASK},
			{"message_type": MessageType.TASK_ASSIGNMENT, "allow_comments": False}
		]
	},
]

async def seed_sections(section_repo: SectionRepository):

	async def _processing(data: Dict[str, Any], parent_id: UUID | None = None):
		code = data["code"]
		allow_hide = data.get("allow_hide", True)
		tech_version = data["tech_version"]
		openai_prompt = data.get("openai_prompt")
		children = data.get("children", [])

		try:
			section = await section_repo.get_by_code(code)
			if section.parent_id != parent_id:
				section.change_parent(parent_id)
		except SectionNotFoundError:
			section = Section.create(
				parent_id=parent_id,
				code=code,
				allow_hide=allow_hide,
				tech_version=tech_version,
				openai_prompt=openai_prompt
			)

		for mt in data.get("message_types", []):
			if section.has_allowed_message_type(mt["message_type"]):
				section.update_allowed_message_type(message_type=mt["message_type"], allow_comments=mt.get("allow_comments", True))
			else:
				section.add_allowed_message_type(message_type=mt["message_type"], allow_comments=mt.get("allow_comments", True))

		current_message_types = {mt.message_type for mt in section.allowed_message_types}
		seed_message_types = {mt["message_type"] for mt in data.get("message_types", [])}

		for message_type in current_message_types - seed_message_types:
			section.remove_allowed_message_type(message_type)

		await section_repo.save(section)

		for child in children:
			await _processing(child, parent_id=section.id)

	for data in SECTIONS:
		await _processing(data)
