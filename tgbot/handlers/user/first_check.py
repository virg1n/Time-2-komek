from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from data import ADMIN_TG_ID
from handlers.user.get_info_from_table import check_user_in_base
from handlers.user.ban_check import check_user_in_ban
from keyboards.admin import admin_main_markup
from keyboards.user import start_registr_markup, menu_markup
from loader import bot
from states import UserData, BannedState


async def check_and_add_registration_button(message: types.Message):
    """Проверка пользователя для последующих действий."""
    if not await check_user_in_base(message):
        await bot.send_message(
            message.from_user.id,
            text=("Welcome to the bot!\n\n"
                  "To select a couple, you need to go through a small registration: "
                  "introduce yourself and answer a couple of questions about yourself, "
                  "to make it easier for the interlocutor to start a conversation with you. If"
                  "if you don't want to answer, then you can skip some of the steps.\n\n"
                  "Click the \"Register\" button below.\n\n"
                  "For communication, help and stories about how it went "
                  "meeting join the cozy bot community in "
                  "telegram https://t.me/+Ai1RweqsyjFhNmFi"
                  ),
            reply_markup=start_registr_markup()
        )
        await UserData.start.set()
    elif message.from_user.id in list(map(int, ADMIN_TG_ID.split())):
        await bot.send_message(
            message.from_user.id,
            text="Hello, Admin. Welcome to the admin menu",
            reply_markup=admin_main_markup(),
        )
    else:
        if not await check_user_in_ban(message):
            await bot.send_message(
                message.from_user.id,
                text="Use the menu",
                reply_markup=menu_markup(message),
            )
        else:
            await bot.send_message(
                message.from_user.id,
                text="Unfortunately, you violated our rules and got banned. "
                     "To resolve this issue, contact the admin "
                     "@Loravel",
                reply_markup=ReplyKeyboardRemove()
            )
            await BannedState.start.set()
