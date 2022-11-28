import ujson
from aiohttp import client_exceptions

from aiohttp.client import ClientSession
from bot.blockchain.base import AbstractBlockchain, Transaction


def _count_transaction_value(transaction: dict) -> int:
    value = 0
    for output in transaction['outputs']:
        value += output['value']
    return value


class BitcoinBlockchain(AbstractBlockchain):
    api_url = "https://chain.api.btc.com/v3"
    explorer = "https://www.blockchain.com"

    def parse_transaction(self, transaction: dict) -> Transaction:
        return Transaction(
            transaction['hash'],
            'Bitcoin',
            _count_transaction_value(transaction),
            f'{self.explorer}/btc/tx/{transaction["hash"]}'
        )

    async def request_last_transaction(self, client: ClientSession, address: str) -> dict:
        request = f'{self.api_url}/address/{address}/tx?pagesize=1'

        async with client.get(request) as response:

            if response.status != 200:
                raise self.InvalidAddress(f"Request failed. Bitcoin responded with status code: {response.status}")

            try:
                json = await response.json(loads=ujson.loads)
            except client_exceptions.ContentTypeError:
                raise self.InvalidAddress(f"Request failed. Bitcoin responded with invalid type.")

            if not json['data']['list']:
                raise self.InvalidAddress(f"Address has no transactions yet")

        return json['data']['list'][0]


