
from dataclasses import dataclass
from aiohttp.client import ClientSession


@dataclass
class Transaction:
    tx_hash: str
    blockchain: str
    amount: int
    explorer_link: str


class AbstractBlockchain:
    async def request_last_transaction(
            self,
            client: ClientSession,
            address: str
    ) -> dict:
        raise NotImplementedError("request_last_transaction was not implemented.")

    def parse_transaction(
            self,
            transaction: dict
    ) -> Transaction:
        raise NotImplementedError("parse_last_transaction was not implemented.")

    class InvalidAddress(Exception):
        def __init__(self, *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
