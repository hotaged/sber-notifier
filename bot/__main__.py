import logging

from rich.logging import RichHandler
from bot import config, db
from bot.handlers.misc import dp
from aiogram.utils import executor


if config.debug:
    logging.basicConfig(level=logging.DEBUG, handlers=[RichHandler()])
else:
    logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])


async def on_startup(*_):
    await db.init()


async def on_shutdown(*_):
    await db.shutdown()


def main(*_, **__):
    uvloop_imported = False

    try:
        import uvloop

        uvloop_imported = True

    except ImportError:
        pass

    if uvloop_imported:
        uvloop.install()

    logging.basicConfig(level=logging.DEBUG)

    executor.start_polling(
        dp,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )


if __name__ == '__main__':
    main()
