import asyncio
import aiohttp
import click
import logging

from bot import db
from bot import blockchain
from bot.handlers import bot
from bot.db.models import SberAddress
from aiogram.utils.markdown import link
from bot.blockchain.base import AbstractBlockchain


async def main(chain: str, delay: float):
    await db.init()

    b_api: AbstractBlockchain = blockchain.choice[chain]

    logging.info("Initiated database.")

    async with aiohttp.ClientSession() as client:
        logging.info("Started polling.")

        while True:
            addresses = await SberAddress.all().prefetch_related("users")

            for address in addresses:
                try:
                    logging.info(f"Polling: {chain.capitalize()}, Address: {address.address}")
                    row_transaction = await b_api.request_last_transaction(client, address.address)
                except b_api.InvalidAddress:
                    continue

                transaction = b_api.parse_transaction(row_transaction)

                if address.last_transaction_id != transaction.tx_hash:

                    message_text = (
                        f"Обнаружена транзакция!\n"
                        f"Блокчейн: {transaction.blockchain}\n"
                        f"Адрес: {address.address}\n"
                        f"Сумма: {transaction.amount}\n"
                        f"{link('Смотреть в блокчейне.', transaction.explorer_link)}\n"
                    )

                    logging.info(f"Polling: {chain.capitalize()}, Address: {address.address} - FOUND!")
                    for user in address.users:
                        await bot.send_message(
                            user.telegram_id,
                            message_text
                        )
                    logging.info(f"Polling: {chain.capitalize()}, Address: {address.address} - Sending complete.")

                    address.last_transaction_id = transaction.tx_hash
                    await address.save()

                await asyncio.sleep(delay)


@click.command()
@click.option(
    '--chain',
    type=click.Choice(list(blockchain.choice.keys()), case_sensitive=False)
)
@click.option(
    '--delay',
    type=click.FLOAT
)
def app(chain: str, delay: float):
    logging.basicConfig(level=logging.INFO)

    logging.info(f"Loaded driver: {chain.capitalize()}")
    asyncio.run(main(chain, delay))


if __name__ == '__main__':
    app()
