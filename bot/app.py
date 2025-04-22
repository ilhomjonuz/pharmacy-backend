import asyncio
import logging
import sys

from loader import dp, bot, db, main_db
import handlers


async def main() -> None:
    await main_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
