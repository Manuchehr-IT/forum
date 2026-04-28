from fastapi import APIRouter, Depends
from typing import List

from src.api.v1.users.dependencies import get_current_user
from src.application.sections.use_cases.list import ListSections
from src.application.users.dtos import UserDTO
from .dependencies import provide_list_sections
from .mappers import ListSectionsMapper
from . import schemas

router = APIRouter(prefix="/sections", tags=["Sections"])

@router.get("", response_model=List[schemas.SectionResponse], summary="Get list sections", description="<b>Получить все секции.</b>")
async def list_sections_endpoint(
	list_sections: ListSections = Depends(provide_list_sections),
	# current_user: UserDTO = Depends(get_current_user),
):
	query = ListSectionsMapper.to_query()
	result_dto_list = await list_sections.execute(query)
	return ListSectionsMapper.to_response(result_dto_list)
