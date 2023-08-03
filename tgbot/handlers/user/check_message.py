from asyncio import sleep

from aiogram.utils.exceptions import BotBlocked

from controllerBD.db_loader import db_session
from controllerBD.models import Users, UserStatus
from handlers.user.get_info_from_table import get_id_from_user_info_table
from loader import bot, logger


async def check_message():
    """Рассылка проверочного сообщения по всем пользователям."""
    logger.info("Starting user verification")
    for user in prepare_user_list():
        await send_message(
            teleg_id=user,
            text="The distribution of pairs will be made very soon.",
        )
        await sleep(0.05)
    logger.info("All users are verified.")


def prepare_user_list():
    """Подготовка списка id пользователей со статусом готов к встрече."""
    logger.info("""Подготавливаем список пользователей из базы""")
    data = db_session.query(Users.teleg_id).join(UserStatus).filter(
        UserStatus.status == 1
    ).all()
    return [element[0] for element in data]


async def send_message(teleg_id, **kwargs):
    """Отправка проверочного сообщения и обработка исключений."""
    try:
        await bot.send_message(teleg_id, **kwargs)
    except BotBlocked:
        logger.error(f"Невозможно доставить сообщение пользователю {teleg_id}."
                     f"Бот заблокирован.")
        await change_status(teleg_id)
    except Exception as error:
        logger.error(f"Невозможно доставить сообщение пользователю {teleg_id}."
                     f"{error}")


async def change_status(teleg_id):
    """Смена статуса участия."""
    user_id = get_id_from_user_info_table(teleg_id)
    db_session.query(UserStatus).filter(UserStatus.id == user_id). \
        update({'status': 0})
