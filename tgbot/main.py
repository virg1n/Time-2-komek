import asyncio
import aioschedule
from aiogram import executor

from data import ADMIN_TG_ID

from handlers.user.holidays import sheduled_check_holidays
from loader import bot, logger, dp

from handlers.user.start_handler import register_start_handler
from handlers.user.new_member import register_new_member_handler
from handlers.user.handlers import register_user_handlers
from handlers.user.help_texts import register_help_texts_handlers
from handlers.user.holidays import register_holidays_handlers
from handlers.user.reviews import register_review_handlers
from handlers.admin.ban_handlers import register_admin_ban_handlers
from handlers.admin.handlers import register_admin_handlers
from handlers.user.review_history import register_review_history_handler
from handlers.user.unknown_message import register_unknown_message_handler

register_start_handler(dp)
register_new_member_handler(dp)
register_user_handlers(dp)
register_help_texts_handlers(dp)
register_holidays_handlers(dp)
register_review_handlers(dp)
register_review_history_handler(dp)
register_admin_ban_handlers(dp)
register_admin_handlers(dp)
register_unknown_message_handler(dp)


async def scheduler():
    """Расписание выполнения задач."""
    aioschedule.every().day.at("09:00").do(sheduled_check_holidays)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(_):
    """Выполняется во время запуска бота."""
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    for i in list(map(int, ADMIN_TG_ID.split())):
        try:
            await bot.send_message(i, 'The bot is running')
        except Exception as error:
            logger.error(f'The message about the launch of the bot did not go away. Mistake {error}')
    logger.info('The bot is running')


async def on_shutdown(_):
    """Выполняется во время остановки бота."""
    for i in list(map(int, ADMIN_TG_ID.split())):
        try:
            await bot.send_message(i, 'Bot stopped')
        except Exception as error:
            logger.error(f'The message about stopping the bot did not go away.'
                         f' Error {error}')
    logger.info('Bot stopped')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown
                           )
