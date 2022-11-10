from aiogram.types import Message
from bot.db.models import TelegramUser
from bot.handlers.misc import dp, bot


@dp.message_handler()
async def any_message(message: Message):
    message_text = (
        "Команды: \n"
        "\n"
        "/sub <адрес>   - Подписка на уведомления о транзакциях адреса.\n"
        "/unsub <адрес> - Отключить уведомления о транзакциях адреса.\n"
        "/subs          - Список адресов."
        "\n"
        "Пример: \n"
        "/sub Sf6tcyxRFL8LjCv3AtPZcYipAHhnPHzrTX"
    )

    await TelegramUser.get_or_create(telegram_id=message.from_user.id)

    return await bot.send_message(
        message.chat.id,
        message_text
    )


