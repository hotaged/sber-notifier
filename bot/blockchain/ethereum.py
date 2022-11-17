import ujson

from aiohttp.client import ClientSession
from bot.blockchain.base import AbstractBlockchain, Transaction


class EthereumBlockchain(AbstractBlockchain):
    api_url = "https://api.etherscan.io/api"
    explorer = "https://etherscan.io"
    api_key = "H4SUADYVE1EQCYB2DW63WNYDZ2DAT26S59"

    def parse_transaction(self, transaction: dict) -> Transaction:
        return Transaction(
            transaction["hash"],
            "Ethereum",
            int(transaction["value"]),
            f'{self.explorer}/tx/{transaction["hash"]}'
        )

    async def request_last_transaction(self, client: ClientSession, address: str) -> dict:
        request = (
            f'{self.api_url}'
            f'?module=account'
            f'&action=txlist'
            f'&address=0xc5102fE9359FD9a28f877a67E36B0F050d81a3CC'
            f'&page=1'
            f'&offset=1'
            f'&sort=desc'
            f'&apikey={self.api_key}'
        )

        async with client.get(request) as response:

            if response.status != 200:
                raise self.InvalidAddress(f"Request failed. Trx scan responded with status code: {response.status}")

            json = await response.json(loads=ujson.loads)

            if not json['result']:
                raise self.InvalidAddress(f"Address has no transactions yet")

        return json['result'][0]



