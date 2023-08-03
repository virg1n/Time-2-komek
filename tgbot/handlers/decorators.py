from aiogram.types import ReplyKeyboardRemove

from data import ADMIN_TG_ID
from handlers.user.ban_check import check_user_in_ban
from handlers.user.get_info_from_table import check_user_in_base
from keyboards.user import start_registr_markup
from loader import bot
from states import UserData


def admin_handlers(func):
    async def wrapped(*args):
        message = list(args)[0]
        if message.from_user.id in list(map(int, ADMIN_TG_ID.split())):
            return await func(*args)
    return wrapped


def user_handlers(func):
    async def wrapped(*args):
        message = list(args)[0]
        if await check_user_in_base(message):
            if not await check_user_in_ban(message):
                return await func(*args)
            else:
                await bot.send_message(
                    message.from_user.id,
                    ("You are banned. Please, "
                     "contact the administrator."),
                    reply_markup=ReplyKeyboardRemove()
                )
        else:
            await bot.send_message(
                message.from_user.id,
                "You're not registered. Enter 'Registration' without quotes "
                "or press the button at the bottom.",
                reply_markup=start_registr_markup(),
                )
            await UserData.start.set()
    return wrapped
