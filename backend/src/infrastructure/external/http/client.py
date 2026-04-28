from httpx import AsyncClient, ConnectTimeout, ConnectError
from tenacity import retry, retry_if_exception_type, wait_exponential, stop_after_attempt

from .enums import HTTPMethod

class HTTPClient:
	def __init__(self, client: AsyncClient):
		self.client = client

	@retry(
		stop=stop_after_attempt(3),
		wait=wait_exponential(multiplier=1, min=1, max=5),
		retry=retry_if_exception_type((ConnectTimeout, ConnectError))
	)
	async def request(self, method: HTTPMethod, url: str, **kwargs):
		response = await self.client.request(method, url, **kwargs)
		response.raise_for_status()
		return response
	
	async def close(self) -> None:
		await self.client.aclose()
