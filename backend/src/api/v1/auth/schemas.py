from pydantic import BaseModel, EmailStr, Field

class TelegramAuthRequest(BaseModel):
	init_data: str = Field(..., description="InitData from Telegram WebApp")

class RegisterByEmailRequest(BaseModel):
	first_name: str = Field(..., min_length=1, max_length=32)
	email: EmailStr
	password: str = Field(..., min_length=8)

class LoginByEmailRequest(BaseModel):
	email: EmailStr
	password: str

class AuthResponse(BaseModel):
	access_token: str = Field(..., description="access_token")
	refresh_token: str | None = Field(..., description="refresh_token")
