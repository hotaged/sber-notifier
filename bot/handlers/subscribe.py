from aiogram.types import Message
from bot.db.models import TelegramUser, SberAddress
from bot.handlers.misc import dp, bot


@dp.message_handler(commands=['sub'])
async def subscribe(message: Message):
    user, _ = await TelegramUser.get_or_create(telegram_id=message.from_user.id)
    address = message.get_args()

    if address is None:
        return await bot.send_message(
            message.chat.id,
            "Не хватает параметра `address`."
        )

    address = address.strip()

    try:
        await user.subscribe(address)

    except SberAddress.ValidationError as ex:
        message_text = (
            "Не удалось загрузить данные об адресе.\n"
            f"Текст ошибки: {ex.message}"
        )
        return await bot.send_message(
            message.chat.id,
            message_text
        )

    message_text = (
        "Успешно добавлено."
    )

    await bot.send_message(
        message.chat.id,
        message_text
    )


@dp.message_handler(commands=['unsub'])
async def unsubscribe(message: Message):
    user, _ = await TelegramUser.get_or_create(telegram_id=message.from_user.id)
    address = message.get_args()

    if address is None:
        return await bot.send_message(
            message.chat.id,
            "Не хватает параметра `address`."
        )

    address = address.strip()

    try:
        await user.unsubscribe(address)

    except TelegramUser.UnsubscribeError as ex:
        message_text = (
            "Не удалось загрузить данные об адресе.\n"
            f"Текст ошибки: {ex.message}"
        )
        return await bot.send_message(
            message.chat.id,
            message_text
        )
    message_text = (
        "Адрес удален."
    )
    await bot.send_message(
        message.chat.id,
        message_text
    )


@dp.message_handler(commands=['subs'])
async def subscriptions(message: Message):
    user, _ = await TelegramUser.get_or_create(telegram_id=message.from_user.id)
    addresses = await user.address_list()

    message_text = "Список адресов: \n"
    for address in addresses:
        message_text += f'<code>{address}</code>'

    return await bot.send_message(
        message.chat.id,
        message_text,
        parse_mode='HTML'
    )
