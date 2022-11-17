import typing

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

from bot import config
from bot.utils import unique_query_id
from bot.handlers.keyboards.base import BUTTON_LIST


BUTTON_LIST_AT = unique_query_id()
BUTTON_LIST_BACK = unique_query_id()


class ListKeyboard(InlineKeyboardMarkup):
    def __init__(self, items: list, offset: int = 0, limit: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        docstring = f'{offset} - {offset + limit} of {len(items)}'

        if offset < limit:
            previous_text = '.'
            previous_query = '*'
        else:
            previous_text = '<'
            previous_query = f'{BUTTON_LIST}.{offset - limit}-{limit}'

        if offset + limit > len(items):
            next_text = '.'
            next_query = '*'
        else:
            next_text = '>'
            next_query = f'{BUTTON_LIST}.{offset + limit}-{limit}'

        self.row(
            InlineKeyboardButton(
                previous_text,
                callback_data=previous_query
            ),
            InlineKeyboardButton(
                docstring,
                callback_data='*'
            ),
            InlineKeyboardButton(
                next_text,
                callback_data=next_query
            ),
        )
        self.add(
            InlineKeyboardButton(
                '<< Назад.',
                callback_data=BUTTON_LIST_BACK
            ),
        )

    @classmethod
    def query_back(cls, query: CallbackQuery) -> bool:
        return query.data == BUTTON_LIST_BACK

    @classmethod
    def query_list_at(cls, query: CallbackQuery) -> bool:
        return query.data.startswith(BUTTON_LIST_AT)

    @classmethod
    def parse_callback_query(cls, callback_query: CallbackQuery) -> typing.Tuple[int, int]:
        offset, limit = tuple(map(int, callback_query.data.split('.')[-1].split('-')))
        return offset, limit

    @classmethod
    def parse_list_index(cls, callback_query: CallbackQuery) -> int:
        return int(callback_query.data.split('.')[-1])
