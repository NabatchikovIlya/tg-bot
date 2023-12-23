import logging

import httpx
from yarl import URL


class ModelRequester:
    MODEL_PATH = "/predict"

    def __init__(self, client: httpx.AsyncClient, base_url: str) -> str:
        self._client = client
        self.base_url = base_url

    async def get_msg(self, msg: str) -> str:
        url = URL.build(
            scheme="http",
            host=self.base_url,
            path=self.MODEL_PATH,
        )
        params = {"message": msg}
        logging.info(f"Send request: {params}")
        response = await self._client.get(str(url), params=params)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            logging.error(f"server error: {e}")
            return "Приносим вам наши извинения, сервис временно недоступен."
        output = response.json()["message"]
        logging.info(f"got response: {output}")
        return output
