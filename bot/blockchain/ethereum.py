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
            f'&address={address}'
            f'&page=1'
            f'&offset=1'
            f'&sort=desc'
            f'&apikey={self.api_key}'
        )

        async with client.get(request) as response:

            if response.status != 200:
                raise self.InvalidAddress(f"Request failed. Trx scan responded with status code: {response.status}")

            json = await response.json(loads=ujson.loads)

            if json['message'] == 'NOTOK':
                raise self.InvalidAddress(f"Address has no transactions yet")

        return json['result'][0]


if __name__ == '__main__':
    import asyncio
    import aiohttp

    async def main():
        async with aiohttp.ClientSession() as client:
            blockchain = EthereumBlockchain()

            try:
                transaction = await blockchain.request_last_transaction(client, 'Sf6tcyxRFL8LjCv3AtPZcYipAHhnPHzrTX')
            except blockchain.InvalidAddress as e:
                return print(e.args)

            print(blockchain.parse_transaction(transaction))

    asyncio.run(main())
