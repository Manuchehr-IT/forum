import asyncio
import uvicorn
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.api.exceptions.handlers import base_app_error_handler, generic_exception_handler, http_exception_handler
from src.api.router import api_router
from src.core.config import settings
from src.shared.exceptions import BaseAppError
# from src.core.exceptions import setup_exception_handlers
# from src.infrastructure.database import db
from src.infrastructure.external.http.client import HTTPClient
from src.infrastructure.logger import logger

async def main() -> None:
	@asynccontextmanager
	async def lifespan(app: FastAPI):
		app.state.http_client = HTTPClient(AsyncClient(timeout=10))
		app.state.redis = Redis.from_url(str(settings.redis.dsn), decode_responses=True)

		app.state.engine = create_async_engine(
			url=str(settings.database.async_dsn),
			echo=settings.debug,
			echo_pool=settings.debug,
			pool_pre_ping=True,
		)

		app.state.session_maker = async_sessionmaker(
			bind=app.state.engine,
			class_=AsyncSession,
			expire_on_commit=False,
			autoflush=True,
		)

		yield

		logger.info("🔴 Shutting down...")

		await app.state.engine.dispose()
		await app.state.redis.aclose()
		await app.state.http_client.close()

	app = FastAPI(
		title=settings.app.title,
		version="1.0.0",
		lifespan=lifespan,
		docs_url="/api/docs" if settings.debug else None,
		swagger_ui_parameters={
			"persistAuthorization": True,
			# "operationsSorter": "method",
		}
	)

	@app.middleware("http")
	async def trace_id_middleware(request: Request, call_next):
		request.state.trace_id = str(uuid.uuid4())
		response = await call_next(request)
		response.headers["X-Trace-Id"] = request.state.trace_id
		return response

	app.add_exception_handler(BaseAppError, base_app_error_handler)
	app.add_exception_handler(HTTPException, http_exception_handler)
	app.add_exception_handler(Exception, generic_exception_handler)
	# setup_exception_handlers(app)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=settings.allowed_origins,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
		expose_headers=["New-Access-Token"]
	)

	app.include_router(api_router)

	config = uvicorn.Config(app=app, host=settings.host, port=settings.port, log_level="info")
	server = uvicorn.Server(config)

	await server.serve()

if __name__ == "__main__":
	asyncio.run(main())
