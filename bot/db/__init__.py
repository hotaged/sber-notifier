from tortoise import Tortoise, connections
from bot import config


async def init():
    await Tortoise.init(
        db_url=config.db_uri,
        modules={'models': ['bot.db.models']}
    )


async def shutdown():
    await connections.close_all()


TORTOISE_ORM = {
    'connections': {'default': config.db_uri},
    'apps': {
        'models': {
            'models': ['bot.db.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}