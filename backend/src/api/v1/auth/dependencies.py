from fastapi import Depends

from src.domain.users.avatar_downloader import AvatarDownloader
from src.api.v1.users.dependencies import get_user_repository
from src.application.auth.use_cases.by_telegram import AuthByTelegram
from src.application.auth.use_cases.by_email import LoginByEmail, RegisterByEmail
from src.domain.users.repository import UserRepository
from src.infrastructure.avatar_downloaders import create_avatar_downloader
from src.infrastructure.auth.password import PasswordHasher
from src.infrastructure.auth.telegram import TelegramInitDataValidator

async def get_tg_validator() -> TelegramInitDataValidator:
	return TelegramInitDataValidator()

async def get_password_hasher() -> PasswordHasher:
	return PasswordHasher()

async def get_auth_by_telegram(
	user_repo: UserRepository = Depends(get_user_repository),
	tg_validator: TelegramInitDataValidator = Depends(get_tg_validator),
	avatar_downloader: AvatarDownloader = Depends(create_avatar_downloader)
) -> AuthByTelegram:
	return AuthByTelegram(user_repo, tg_validator, avatar_downloader)

async def get_register_by_email(
	user_repo: UserRepository = Depends(get_user_repository),
	password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> RegisterByEmail:
	return RegisterByEmail(user_repo, password_hasher)

async def get_login_by_email(
	user_repo: UserRepository = Depends(get_user_repository),
	password_hasher: PasswordHasher = Depends(get_password_hasher),
) -> LoginByEmail:
	return LoginByEmail(user_repo, password_hasher)
