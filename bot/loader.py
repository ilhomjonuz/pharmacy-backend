from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.database import Apteka_Database
from bot.data.config import BOT_TOKEN


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Apteka_Database()


async def main_db():
    await db.connect()
