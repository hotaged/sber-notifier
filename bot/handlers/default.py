import aiohttp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from bot.db.models import TelegramUser, BlockchainAddress
from bot.handlers.misc import dp, bot

from bot.handlers.keyboards.base import BaseKeyboard
from bot.handlers.keyboards.list import ListKeyboard
from bot.blockchain import choice as blockchains

BASE_MESSAGE_TEXT = (
    "Отслеживайте активность интересующих вас адресов в блокчейнах Bitcoin, Ethereum, Sbercoin.com, Tron, "
    "Dogecoin в режиме реального времени. "
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


@dp.callback_query_handler(lambda x: x.data == '*')
async def callback_query_any(callback_query: CallbackQuery):
    return await bot.answer_callback_query(callback_query.id)


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

    await state.finish()
    address = address.strip()

    loading_message = await bot.send_message(
        message.chat.id,
        f"⏳ Ищу адрес: {address}"
    )

    blockchain_found = False
    async with aiohttp.ClientSession() as client:
        for blockchain in blockchains:
            loading_message = await bot.edit_message_text(
                f"⏳ Ищу адрес: {address} на блокчейне {blockchain}",
                message.chat.id,
                loading_message.message_id
            )
            try:
                raw_tx = await blockchains[blockchain].request_last_transaction(client, address)
                transaction = blockchains[blockchain].parse_transaction(raw_tx)
                chain_address, _ = await BlockchainAddress.get_or_create(address=address)
                await chain_address.init_address(blockchain, transaction.tx_hash)
                blockchain_found = True
                break
            except blockchains[blockchain].InvalidAddress:
                continue

    await bot.delete_message(
        message.chat.id,
        loading_message.message_id
    )

    if not blockchain_found:
        message_text = (
            "Не удалось загрузить данные об адресе.\n"
            "Проверьте правильность написания адреса."
        )
        await bot.send_message(
            message.chat.id,
            message_text
        )
        return await any_message(message)

    try:
        await user.subscribe(address)

    except BlockchainAddress.ValidationError as ex:
        message_text = (
            "Не удалось загрузить данные об адресе.\n"
            f"Текст ошибки: {ex.message}"
        )
        return await bot.send_message(
            message.chat.id,
            message_text
        )

    message_text = (
        "Успешно добавлено.\n"
        f"Блокчейн: {transaction.blockchain}"
    )

    await bot.send_message(
        message.chat.id,
        message_text
    )

    await any_message(message)


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
    address = message.text

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
    addresses = await BlockchainAddress.as_list_items(users=user)

    message_text = "Список адресов: \n"
    for address, i in addresses[offset:offset + limit]:
        message_text += f'--- <code>{address}</code>\n'

    return await bot.edit_message_text(
        message_text,

        callback_query.message.chat.id,
        callback_query.message.message_id,
        callback_query.inline_message_id,

        reply_markup=ListKeyboard(
            addresses, offset, limit
        ),

        parse_mode='HTML'
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

    await bot.send_message(
        callback_query.message.chat.id,
        (
            "Добавить адрес: \n"
            "Чтобы добавить новый адрес для отслеживания просто вставьте адрес одного из поддерживаемых блокчейнов ("
            "Bitcoin, Ethereum, Sbercoin.com, Tron, Dogecoin) \n"
            "Удалить адрес: \n"
            "Чтобы удалить ранее добавленный адрес из отслеживаемых\n"
            "Лист адресов: \n"
            "Список всех отслеживаемых адресов"
        ))

    await any_message(callback_query.message)
