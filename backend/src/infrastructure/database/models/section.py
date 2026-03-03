import uuid
from sqlalchemy import Boolean, ForeignKey, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base, TimestampMixin

class SectionModel(Base, TimestampMixin):
	__tablename__ = "sections"

	parent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id", ondelete="RESTRICT"), nullable=True)
	code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
	openai_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
	tech_version: Mapped[str] = mapped_column(Text, nullable=False)
	enable_openai: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
	allow_hide: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

	# allowed_message_types: Mapped[List["SectionMessageTypeModel"]] = relationship(
	# 	back_populates="section", 
	# 	cascade="all, delete-orphan"
	# )
