from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import Dispatcher

from handlers.decorators import user_handlers
from keyboards.user import help_texts
from loader import bot

help_texts_messages = [
    ("Hi! I'm your buddy this week. "
     "How about going out for coffee together on the weekend?"),
    "Hello! When do you have time this week?",
    ("Hi! The bot writes that you are my interlocutor for this week. "
     "We can meet or call. How is it convenient for you?"),
    ("Good afternoon! You fell to me in the bot. "
     "Tell me, when will it be convenient for you to call?"),
    ("Greetings! I will be glad to meet you, but I have a little "
     "the second half of the week is loaded. "
     "Maybe we can do it on Tuesday or Wednesday?")
]


# @dp.message_handler(text=help_texts)
@user_handlers
async def send_help_texts(message: types.Message):
    """Отправка сообщений примеров."""
    await bot.send_message(
        message.from_user.id,
        "You can copy the text by clicking on it."
    )
    for text in help_texts_messages:
        await sleep(0.05)
        await bot.send_message(message.from_user.id,
                               f'<code>{text}</code>',
                               parse_mode='HTML')


def register_help_texts_handlers(dp: Dispatcher):
    dp.register_message_handler(send_help_texts, text=help_texts)
