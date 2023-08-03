from asyncio import sleep

from aiogram import Bot

from controllerBD.db_loader import db_session
from controllerBD.models import Users, Gender
from controllerBD.services import get_defaulf_pare_base_id, update_mets, \
    update_all_user_mets, get_tg_username_from_db_by_teleg_id
from handlers.user.work_with_date import date_from_db_to_message
from keyboards.user import help_texts_markup
from loader import logger


async def send_match_messages(match_info: dict, bot: Bot):
    """Рассылка сообщений после распределения пар на неделю."""
    for match in match_info.items():
        await sleep(0.1)
        users_info = pare_users_query(match)
        if not users_info:
            logger.error(f'Failed to get information '
                         f'from the database for a couple {match}')
            continue
        elif len(users_info) == 2:
            first_user = users_info[0]
            first_user_id = first_user[1]
            second_user = users_info[1]
            second_user_id = second_user[1]
            try:
                first_message = make_message(first_user)
            except Exception as error:
                logger.error(f'Failed to generate a message about'
                             f'the user {first_user}. Error {error}')
            try:
                second_message = make_message(second_user)
            except Exception as error:
                logger.error(f'Failed to generate a message about '
                             f'the user {second_user}. Error {error}')
            try:
                await bot.send_message(second_user_id, first_message,
                                       parse_mode="HTML",
                                       reply_markup=help_texts_markup())
                logger.info(f'Message to the user {second_user_id} '
                            f'sended')
            except Exception as error:
                logger.error(f'Message to the user  {second_user_id} '
                             f'unsended. Error {error}')
            try:
                await bot.send_message(first_user_id, second_message,
                                       parse_mode="HTML",
                                       reply_markup=help_texts_markup())
                logger.info(f'Message to the user {first_user_id} '
                            f'shipped')
            except Exception as error:
                logger.error(f'Message to the user  {first_user_id} '
                             f'not sent. Error{error}')
        else:
            fail_user = users_info[0]
            fail_user_db_id = fail_user[0]
            default_user_db_id = get_defaulf_pare_base_id()
            fail_match = {fail_user_db_id: default_user_db_id}
            await update_mets(fail_match)
            update_all_user_mets(fail_match)
            await send_match_messages(fail_match, bot)

    logger.info("Completion of sending messages about new meetings")


def make_message(user_info: tuple) -> str:
    """Формирует сообщение о паре для отправки."""
    user_id = user_info[1]
    user_name = user_info[2]
    user_birthday = user_info[3]
    if user_birthday == "Not specified":
        pass
    else:
        user_birthday = date_from_db_to_message(user_birthday)
    user_about = user_info[4]
    user_gender = user_info[5]
    user_tg_username = get_tg_username_from_db_by_teleg_id(user_id)

    base_message = (f'На этой неделе твоя пара для кофе: '
                    f'<a href="tg://user?id={user_id}">{user_name}</a>')
    tg_username_message = (f'@{user_tg_username}')
    birth_day_message = f'Birthday: {user_birthday}'
    about_message = f'Data: {user_about}'
    gender_message = f'Sex: {user_gender}'
    row_message_list = [base_message]

    if user_tg_username:
        row_message_list.append(tg_username_message)
    if user_birthday != 'Not specified':
        row_message_list.append(birth_day_message)
    if user_about != 'Not specified':
        row_message_list.append(about_message)
    if user_gender != 'Not specified':
        row_message_list.append(gender_message)
    message = '\n'.join(row_message_list)

    return message


def pare_users_query(pare: tuple):
    """Запрашивает информацию по паре юзеров из базы."""
    try:
        result = db_session.query(
            Users.id,
            Users.teleg_id,
            Users.name,
            Users.birthday,
            Users.about,
            Gender.gender_name
        ).join(Gender).filter(Users.id.in_(pare)).all()
    except Exception:
        result = None
    finally:
        return result
