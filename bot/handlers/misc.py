from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot import config

memory = MemoryStorage()

bot = Bot(config.token)
dp = Dispatcher(bot, storage=memory)
