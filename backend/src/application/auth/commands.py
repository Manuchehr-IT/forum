from pydantic import BaseModel

class AuthByTelegramCommand(BaseModel):
	init_data: str

class RegisterByEmailCommand(BaseModel):
	first_name: str
	email: str
	password: str

class LoginByEmailCommand(BaseModel):
	email: str
	password: str
