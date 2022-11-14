import aiohttp
import ujson
from tortoise import models, fields
from bot.db.mixins import AsListItemMixin

from bot import config


class TelegramUser(models.Model):
    telegram_id = fields.BigIntField(unique=True)
    is_admin = fields.BooleanField(default=False)

    addresses: fields.ManyToManyRelation['SberAddress'] = fields.ManyToManyField(
        "models.SberAddress", related_name="users"
    )

    def __str__(self) -> str:
        return f'User<id: {self.telegram_id}>'

    class UnsubscribeError(Exception):
        def __init__(self, message):
            self.message = message

    async def subscribe(self, address: str):
        sber_address = await SberAddress.get_or_none(address=address)

        if sber_address is None:
            sber_address = await SberAddress.from_address(address)

        await self.addresses.add(sber_address)

    async def unsubscribe(self, address: str):
        sber_address = await SberAddress.get_or_none(address=address)

        if sber_address is None:
            raise self.UnsubscribeError("Not found")

        await self.addresses.remove(sber_address)

    async def address_list(self) -> list[str]:
        return await self.addresses.all().values_list("address", flat=True)


class SberAddress(models.Model, AsListItemMixin):
    address = fields.CharField(max_length=64, unique=True)
    last_transaction_id = fields.CharField(max_length=64, null=True)

    users: fields.ManyToManyRelation[TelegramUser]

    def __str__(self):
        return self.address

    class ValidationError(Exception):
        def __init__(self, message: str):
            self.message = message

    @classmethod
    async def from_address(cls, address: str) -> 'SberAddress':
        async with aiohttp.ClientSession() as client:
            request = f'{config.sber_explorer_api}/address/{address}/basic-txs?limit=1&offset=0'

            async with client.get(request) as response:
                if response.status != 200:
                    raise cls.ValidationError(f'Sbercoin explorer responded with status: {response.status}')

                json = await response.json(loads=ujson.loads)

        if not json['totalCount']:
            return await cls.create(address=address)

        return await cls.create(address=address, last_transaction_id=json['transactions'][0]['id'])


