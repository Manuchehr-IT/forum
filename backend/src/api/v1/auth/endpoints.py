from fastapi import APIRouter, Depends

from . import schemas
from src.api.v1.auth.dependencies import get_auth_by_telegram, get_login_by_email, get_register_by_email
from src.application.auth.commands import AuthByTelegramCommand, LoginByEmailCommand, RegisterByEmailCommand
from src.application.auth.use_cases.by_email import LoginByEmail, RegisterByEmail
from src.application.auth.use_cases.by_telegram import AuthByTelegram

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/telegram", response_model=schemas.AuthResponse)
async def auth_telegram_endpoint(
	payload: schemas.TelegramAuthRequest,
	auth_by_telegram: AuthByTelegram = Depends(get_auth_by_telegram)
):
	command = AuthByTelegramCommand(**payload.model_dump())
	result = await auth_by_telegram.execute(command=command)
	return schemas.AuthResponse(access_token=result.access_token, refresh_token=result.refresh_token)

@router.post("/register", response_model=schemas.AuthResponse, status_code=201)
async def register_by_email_endpoint(
	payload: schemas.RegisterByEmailRequest,
	register: RegisterByEmail = Depends(get_register_by_email)
):
	command = RegisterByEmailCommand(**payload.model_dump())
	result = await register.execute(command=command)
	return schemas.AuthResponse(access_token=result.access_token, refresh_token=result.refresh_token)

@router.post("/login", response_model=schemas.AuthResponse)
async def login_by_email_endpoint(
	payload: schemas.LoginByEmailRequest,
	login: LoginByEmail = Depends(get_login_by_email)
):
	command = LoginByEmailCommand(**payload.model_dump())
	result = await login.execute(command=command)
	return schemas.AuthResponse(access_token=result.access_token, refresh_token=result.refresh_token)
