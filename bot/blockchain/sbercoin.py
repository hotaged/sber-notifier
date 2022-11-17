import ujson

from aiohttp.client import ClientSession
from bot.blockchain.base import AbstractBlockchain, Transaction


class SbercoinBlockchain(AbstractBlockchain):
    api_url = "https://explorer.sbercoin.com/api"
    explorer_url = "https://explorer.sbercoin.com"

    def parse_transaction(self, transaction: dict) -> Transaction:
        return Transaction(
            transaction['id'],
            'Sbercoin',
            abs(int(transaction['amount'])),
            f'{self.explorer_url}/tx/{transaction["id"]}'
        )

    async def request_last_transaction(self, client: ClientSession, address: str) -> dict:
        request = f'{self.api_url}/address/{address}/basic-txs?limit=1&offset=0'

        async with client.get(request) as response:

            if response.status != 200:
                raise self.InvalidAddress(f"Request failed. Sbercoin responded with status code: {response.status}")

            json = await response.json(loads=ujson.loads)

            if not json['transactions']:
                raise self.InvalidAddress(f"Address doesn't exists.")

        return json['transactions'][0]


