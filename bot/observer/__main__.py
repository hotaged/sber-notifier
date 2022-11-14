import asyncio
import aiohttp
import ujson
import logging

from bot import db, config
from bot.handlers import bot
from bot.db.models import SberAddress


async def main(delay: float):
    await db.init()

    logging.info("Initiated database.")

    async with aiohttp.ClientSession() as client:

        while True:
            addresses = await SberAddress.all().prefetch_related("users")

            for address in addresses:
                request = f'{config.sber_explorer_api}/address/{address.address}/basic-txs?limit=1&offset=0'

                async with client.get(request) as response:
                    logging.info(f"Requesting address: {address.address}")

                    json = await response.json(loads=ujson.loads)

                    logging.info(f"Got response: {json}")

                if not json['transactions']:
                    continue

                transaction_id = json['transactions'][0]['id']

                if address.last_transaction_id != transaction_id:

                    message_text = (
                        f"Новая транзакция по адресу {address.address}!\n"
                        f"{config.sber_explorer_url}/tx/{transaction_id}"
                    )

                    for user in address.users:
                        await bot.send_message(
                            user.telegram_id,
                            message_text
                        )

                    address.last_transaction_id = transaction_id
                    await address.save()

                await asyncio.sleep(delay)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(0.1))