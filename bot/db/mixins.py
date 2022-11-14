import typing


class AsListItemMixin:

    @classmethod
    async def as_list_items(cls, *args, **kwargs) -> typing.List[typing.Tuple[str, int]]:
        return list(map(lambda instance: (instance.__str__(), instance.id), await cls.filter(*args, **kwargs)))
