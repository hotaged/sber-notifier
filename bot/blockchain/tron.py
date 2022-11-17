import ujson

from aiohttp.client import ClientSession
from bot.blockchain.base import AbstractBlockchain, Transaction


class TronBlockchain(AbstractBlockchain):
    api_url = "https://apilist.tronscan.org/api"
    explorer = "https://tronscan.org"

    def parse_transaction(self, transaction: dict) -> Transaction:
        return Transaction(
            transaction['hash'],
            'Tron',
            int(transaction["amount"]),
            f'{self.explorer}/#/transaction/{transaction["hash"]}'
        )

    async def request_last_transaction(self, client: ClientSession, address: str) -> dict:
        request = (
            f'{self.api_url}/transaction'
            '?sort=-timestamp'
            '&count=true'
            '&limit=1'
            '&start=0'
            f'&address={address}'
        )

        async with client.get(request) as response:

            if response.status != 200:
                raise self.InvalidAddress(f"Request failed. Trx scan responded with status code: {response.status}")

            json = await response.json(loads=ujson.loads)

            if not json['data']:
                raise self.InvalidAddress(f"Address has no transactions yet")

        return json['data'][0]

