from src.application.decorators import handle_domain_errors
from src.application.auth.commands import LoginByEmailCommand, RegisterByEmailCommand
from src.application.auth.dtos import AuthResultDTO
from src.application.auth.exceptions import AuthFailedError
from src.domain.users.entities.user import User
from src.domain.users.exceptions import EmailAlreadyExistsError, UserNotFoundError
from src.domain.users.repository import UserRepository
from src.infrastructure.auth.jwt import JWTManager
from src.infrastructure.auth.password import PasswordHasher


class RegisterByEmail:
	def __init__(self, user_repo: UserRepository, password_hasher: PasswordHasher):
		self.user_repo = user_repo
		self.password_hasher = password_hasher

	@handle_domain_errors
	async def execute(self, command: RegisterByEmailCommand) -> AuthResultDTO:
		try:
			await self.user_repo.get_by_email(command.email)
			raise EmailAlreadyExistsError(command.email)
		except UserNotFoundError:
			pass

		password_hash = self.password_hasher.hash(command.password)
		user = User.create_from_email(
			first_name=command.first_name,
			email=command.email,
			password_hash=password_hash,
		)
		await self.user_repo.add(user)

		access_token = JWTManager.create_access_token({"sub": str(user.id), "provider": "email"})
		refresh_token = JWTManager.create_refresh_token(user.id)
		return AuthResultDTO(access_token=access_token, refresh_token=refresh_token)


class LoginByEmail:
	def __init__(self, user_repo: UserRepository, password_hasher: PasswordHasher):
		self.user_repo = user_repo
		self.password_hasher = password_hasher

	@handle_domain_errors
	async def execute(self, command: LoginByEmailCommand) -> AuthResultDTO:
		try:
			user = await self.user_repo.get_by_email(command.email)
		except UserNotFoundError:
			raise AuthFailedError("Invalid email or password")

		if not user.password_hash or not self.password_hasher.verify(command.password, user.password_hash):
			raise AuthFailedError("Invalid email or password")

		access_token = JWTManager.create_access_token({"sub": str(user.id), "provider": "email"})
		refresh_token = JWTManager.create_refresh_token(user.id)
		return AuthResultDTO(access_token=access_token, refresh_token=refresh_token)
