from asyncpg import Pool
from asyncpg.pool import PoolConnectionProxy
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from typing import AsyncIterator

from src.domain.interfaces.llm_service import LLMService
from src.domain.users.exceptions import InvalidTokenError, TokenExpiredError
from src.infrastructure.auth.jwt import JWTManager
from src.infrastructure.database import UnitOfWork, db
from src.infrastructure.external.http import HTTPClient
from src.infrastructure.services.openai.factory import create_openai_service

security = HTTPBearer(auto_error=False)

async def get_http_client(request: Request) -> HTTPClient:
	return request.app.state.http_client

async def get_redis(request: Request) -> Redis:
	return request.app.state.redis

async def get_engine_client(request: Request) -> AsyncEngine:
	return request.app.state.engine

async def get_session_factory(request: Request) -> async_sessionmaker:
	return request.app.state.session_maker

async def get_uow(
	session_factory: async_sessionmaker = Depends(get_session_factory)
) -> UnitOfWork:
	return UnitOfWork(session_factory)

async def get_token_payload(
	credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
	"""Базовый dependency для получения payload из токена"""
	try:
		return JWTManager.verify_token(credentials.credentials)
	except (InvalidTokenError, TokenExpiredError) as e:
		raise HTTPException(
			status_code=401,
			detail={
				"code": e.error_code,
				"message": e.message
			},
			headers={"WWW-Authenticate": "Bearer"},
		)

async def get_db_connection() -> AsyncIterator[PoolConnectionProxy]:
	async with db.get_connection() as conn:
		yield conn

async def get_db_pool() -> Pool:
	"""Зависимость для получения пула соединений"""
	if db._pool is None:
		await db.connect()
	return db.pool


async def get_llm_service() -> LLMService:
	return create_openai_service()
