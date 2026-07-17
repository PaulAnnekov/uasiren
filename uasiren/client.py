from aiohttp import ClientSession, ClientResponse


class Client:
    """Class to make authenticated requests."""

    BASE_PATH = "https://siren.pp.ua/api/v3"
    REQUEST_TIMEOUT = 30

    def __init__(self, session: ClientSession, timeout: float = None):
        """Initialize the client.

        :param timeout: total request timeout in seconds,
            defaults to Client.REQUEST_TIMEOUT
        """
        self.session = session
        self.timeout = timeout if timeout is not None else Client.REQUEST_TIMEOUT

    async def __request(self, method: str, path: str) -> ClientResponse:
        """Make a request."""

        headers = {
            "accept": "application/json"
        }

        r = await self.session.request(
            method,
            f"{Client.BASE_PATH}/{path}",
            headers=headers,
            timeout=self.timeout
        )
        r.raise_for_status()
        return await r.json()

    async def get_alerts(self, region_id: str = None) -> ClientResponse:
        """Get alerts."""
        return await self.__request("GET", "alerts" if region_id is None else f"alerts/{region_id}")

    async def get_last_alert_index(self) -> ClientResponse:
        """Get last alert index."""
        return await self.__request("GET", "alerts/status")

    async def get_regions(self) -> ClientResponse:
        """Get regions."""
        return await self.__request("GET", "regions")
