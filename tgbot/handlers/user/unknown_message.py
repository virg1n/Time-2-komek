from aiogram import types, Dispatcher

from handlers.decorators import user_handlers
from keyboards.user import menu_markup
from loader import bot


# @dp.message_handler(state="*")
@user_handlers
async def unknown_message(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        "I don't understand you. Please use the menu.",
        reply_markup=menu_markup(message)
    )


def register_unknown_message_handler(dp: Dispatcher):
    dp.register_message_handler(unknown_message, state="*")
