from tortoise import models, fields
from bot.db.mixins import AsListItemMixin


class TelegramUser(models.Model):
    telegram_id = fields.BigIntField(unique=True)
    is_admin = fields.BooleanField(default=False)

    addresses: fields.ManyToManyRelation['BlockchainAddress'] = fields.ManyToManyField(
        "models.BlockchainAddress", related_name="users"
    )

    def __str__(self) -> str:
        return f'User<id: {self.telegram_id}>'

    class UnsubscribeError(Exception):
        def __init__(self, message):
            self.message = message

    async def subscribe(self, address: str):
        sber_address = await BlockchainAddress.get_or_none(address=address)

        if sber_address is None:
            sber_address = await BlockchainAddress.from_address(address)

        await self.addresses.add(sber_address)

    async def unsubscribe(self, address: str):
        sber_address = await BlockchainAddress.get_or_none(address=address)

        if sber_address is None:
            raise self.UnsubscribeError("Not found")

        await self.addresses.remove(sber_address)

    async def address_list(self) -> list[str]:
        return await self.addresses.all().values_list("address", flat=True)


class BlockchainAddress(models.Model, AsListItemMixin):
    address = fields.CharField(max_length=256, unique=True)
    last_transaction_id = fields.CharField(max_length=256, null=True)
    chain = fields.CharField(max_length=16, null=True)

    users: fields.ManyToManyRelation[TelegramUser]

    def __str__(self):
        return self.address

    class ValidationError(Exception):
        def __init__(self, message: str):
            self.message = message

    @classmethod
    async def from_address(cls, address: str) -> 'BlockchainAddress':
        return await cls.create(address=address)

    async def init_address(self, chain: str, last_transaction_id: str):
        self.chain, self.last_transaction_id = chain, last_transaction_id
        await self.save()


