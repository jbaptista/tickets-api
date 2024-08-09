from httpx import AsyncClient


class AccountClient:
    max_id = 10

    def __init__(self, base_url: str):
        self.client = AsyncClient(base_url=base_url)

    async def get_account_name(self, account_id: int) -> str:
        response = await self.client.get(f"/users/{account_id}")
        response.raise_for_status()
        return response.json()["name"]
