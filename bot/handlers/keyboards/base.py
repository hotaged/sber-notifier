from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from bot.utils import unique_query_id


BUTTON_ADD = unique_query_id()
BUTTON_DELETE = unique_query_id()
BUTTON_LIST = unique_query_id()
BUTTON_INSTRUCTION = unique_query_id()


class BaseKeyboard(InlineKeyboardMarkup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add(InlineKeyboardButton(
            "🟢 Добавить.", callback_data=BUTTON_ADD
        ))
        self.add(InlineKeyboardButton(
            "🔻 Удалить.", callback_data=BUTTON_DELETE
        ))
        self.add(InlineKeyboardButton(
            "🗒 Лист адресов.", callback_data=f"{BUTTON_LIST}.0-5"
        ))
        self.add(InlineKeyboardButton(
            "🐹 Инструкция.", callback_data=BUTTON_INSTRUCTION
        ))

    @classmethod
    def query_add(cls, query: CallbackQuery) -> bool:
        return query.data == BUTTON_ADD

    @classmethod
    def query_delete(cls, query: CallbackQuery) -> bool:
        return query.data == BUTTON_DELETE

    @classmethod
    def query_list(cls, query: CallbackQuery) -> bool:
        return query.data.startswith(BUTTON_LIST)

    @classmethod
    def query_instruction(cls, query: CallbackQuery) -> bool:
        return query.data == BUTTON_INSTRUCTION
