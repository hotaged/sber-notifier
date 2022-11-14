from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from bot.db.models import TelegramUser, SberAddress
from bot.handlers.misc import dp, bot

from bot.handlers.keyboards.base import BaseKeyboard
from bot.handlers.keyboards.list import ListKeyboard


BASE_MESSAGE_TEXT = (
        "Команды: \n"
        "\n"
        "/sub <адрес>   - Подписка на уведомления о транзакциях адреса.\n"
        "/unsub <адрес> - Отключить уведомления о транзакциях адреса.\n"
        "/subs          - Список адресов."
        "\n"
        "Пример: \n"
        "/sub Sf6tcyxRFL8LjCv3AtPZcYipAHhnPHzrTX"
    )


@dp.message_handler()
async def any_message(message: Message):
    await TelegramUser.get_or_create(telegram_id=message.chat.id)

    return await bot.send_message(
        message.chat.id,
        BASE_MESSAGE_TEXT,
        reply_markup=BaseKeyboard()
    )


class AddAddressForm(StatesGroup):
    started = State()


class RemoveAddressForm(StatesGroup):
    started = State()


@dp.callback_query_handler(BaseKeyboard.query_add)
async def callback_query_add(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.message.chat.id,
        "Отправьте мне адрес."
    )
    await AddAddressForm.started.set()


@dp.message_handler(state=AddAddressForm.started)
async def handle_address(message: Message, state: FSMContext):
    user, _ = await TelegramUser.get_or_create(telegram_id=message.chat.id)

    address = message.text

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

    await any_message(message)
    await state.finish()


@dp.callback_query_handler(BaseKeyboard.query_delete)
async def callback_query_delete(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.message.chat.id,
        "Отправьте мне адрес."
    )
    await RemoveAddressForm.started.set()


@dp.message_handler(state=RemoveAddressForm.started)
async def handle_delete(message: Message, state: FSMContext):
    user, _ = await TelegramUser.get_or_create(telegram_id=message.chat.id)
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

    await any_message(message)
    await state.finish()


@dp.callback_query_handler(BaseKeyboard.query_list)
async def callback_query_list(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    user, _ = await TelegramUser.get_or_create(telegram_id=callback_query.message.chat.id)
    offset, limit = ListKeyboard.parse_callback_query(callback_query)
    addresses = await SberAddress.as_list_items(users__in=[user])

    return await bot.edit_message_text(
        BASE_MESSAGE_TEXT,

        callback_query.message.chat.id,
        callback_query.message.message_id,
        callback_query.inline_message_id,

        reply_markup=ListKeyboard(
            addresses, offset, limit
        )
    )


@dp.callback_query_handler(ListKeyboard.query_back)
async def callback_query_list_back(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    return await bot.edit_message_text(
        BASE_MESSAGE_TEXT,

        callback_query.message.chat.id,
        callback_query.message.message_id,
        callback_query.inline_message_id,

        reply_markup=BaseKeyboard()
    )


@dp.callback_query_handler(BaseKeyboard.query_instruction)
async def callback_query_inst(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
