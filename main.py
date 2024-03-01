from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from core.handlers.basic import get_start
from core.settings import settings
import asyncio
import logging

from utils.commands import set_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers import apsscheduler
from utils.reset_counter import reset_counter


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен!')


async def start():
    logging.basicConfig(level=logging.INFO, filename=datetime.now().strftime('logs/pythonFriendPhotoBot_%d-%m-%Y.log'),
                        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%("
                               "funcName)s(%(lineno)d) - %(message)s", encoding="UTF-8")
    bot = Bot(token=settings.bots.bot_token)

    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone="Europe/Samara")

    scheduler.add_job(apsscheduler.send_photo_interval, trigger='cron', hour='10-22', kwargs={'bot': bot})
    scheduler.add_job(apsscheduler.send_quotes_interval, trigger='cron', hour='9', kwargs={'bot': bot})
    scheduler.start()
    dp.startup.register(reset_counter)
    # dp.shutdown.register(stop_bot)
    # dp.message.register(send_media.get_photo, Command(commands='photo'))

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
