from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from database import Database
from data.config import BOT_TOKEN



bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
db = Database()


async def main_db():
    await db.connect()
