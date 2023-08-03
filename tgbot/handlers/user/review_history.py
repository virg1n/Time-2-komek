from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from sqlalchemy import or_, desc, and_
from sqlalchemy.exc import NoResultFound

from controllerBD.db_loader import db_session
from controllerBD.models import MetInfo, MetsReview
from controllerBD.services import get_tg_username_from_db_by_base_id
from handlers.decorators import user_handlers
from handlers.user.add_username import check_username
from handlers.user.get_info_from_table import get_id_from_user_info_table, \
    get_user_info_by_id
from handlers.user.work_with_date import date_from_db_to_message
from keyboards.user import review_yes_or_no, my_reviews
from loader import bot, logger
from states import ReviewState

review_callbackdata = CallbackData("dun_w", "position", "edit")


def list_of_user_mets_id(user_id):
    """Получение id всех встреч пользователя."""
    met_ids = db_session.query(MetInfo.id).filter(
        or_(MetInfo.first_user_id == user_id,
            MetInfo.second_user_id == user_id)
    ).order_by(desc(MetInfo.id)).limit(10).all()
    return [met_id[0] for met_id in met_ids]


# @dp.message_handler(text=my_reviews)
@user_handlers
async def get_my_reviews(message: types.Message):
    """Выводим карточку с последней встречей"""
    await check_username(message)
    user_id = get_id_from_user_info_table(message.from_user.id)
    met_ids = list_of_user_mets_id(user_id)
    count_of_mets = len(met_ids)
    if count_of_mets == 0:
        await bot.send_message(message.from_user.id,
                               "You haven't had any meetings yet.")
    else:
        met_id = met_ids[0]
        review_info = get_sqliterow_review(met_id, user_id)
        if review_info:
            edit_button = "Edit feedback"
        else:
            edit_button = "Add feedback"
        message_text = prepare_message(user_id, met_id, review_info)
        await bot.send_message(message.from_user.id, message_text,
                               parse_mode='HTML',
                               reply_markup=inline_markup(count_of_mets, 0,
                                                          edit_button))
        logger.info(f'User {message.from_user.id} got infromation'
                    f'about last meeting {met_id}')


# @dp.callback_query_handler(review_callbackdata.filter())
async def button_press(call: types.CallbackQuery, callback_data: dict,
                       state: FSMContext):
    """Выводим информацию о встрече в зависимости от позиции."""
    position = int(callback_data.get('position'))
    user_id = get_id_from_user_info_table(call.from_user.id)
    met_ids = list_of_user_mets_id(user_id)
    count_of_mets = len(met_ids)
    met_id = met_ids[position]
    review_info = get_sqliterow_review(met_id, user_id)
    if review_info:
        edit_button = "Edit feedback"
    else:
        edit_button = "Add feedback"
    if int(callback_data.get('edit')) == 1:
        await call.answer()
        await bot.edit_message_reply_markup(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        await bot.send_message(
            call.from_user.id,
            "Did your meeting take place?",
            reply_markup=review_yes_or_no()
        )
        logger.info(f'Пользователь {call.from_user.id} начал редактировать '
                    f'отзыв о встрече {met_id}')
        await ReviewState.start.set()
        user_id = get_id_from_user_info_table(call.from_user.id)
        await state.update_data(user_id=user_id)
        await state.update_data(met_id=met_id)
    else:
        message_text = prepare_message(user_id, met_id, review_info)
        await bot.edit_message_text(message_text, call.from_user.id,
                                    call.message.message_id, parse_mode='HTML',
                                    reply_markup=inline_markup(count_of_mets,
                                                               position,
                                                               edit_button))
        logger.info(f'Пользователь {call.from_user.id} получил информация '
                    f'о последней встрече {met_id}')


def inline_markup(count_of_mets, position, edit_button):
    """Инлайн-кнопки для карточки встречи."""
    markup = InlineKeyboardMarkup(row_width=3)
    if position < (count_of_mets - 1):
        markup.insert(InlineKeyboardButton(
            "Prev.",
            callback_data=review_callbackdata.new(
                position=position+1,
                edit=0
            )))
    markup.insert(InlineKeyboardButton(
        f"{edit_button}",
        callback_data=review_callbackdata.new(
            position=position,
            edit=1
        )))
    if position > 0:
        markup.insert(InlineKeyboardButton(
            "Next.",
            callback_data=review_callbackdata.new(
                position=position-1,
                edit=0
            )))

    return markup


def prepare_message(user_id, met_id, review_info):
    """Подготавливаем сообщение о встрече с коментарием."""
    met_info = get_sqliterow_about_met(met_id)
    date = date_from_db_to_message(met_info['date'])
    if met_info['first_user_id'] == user_id:
        pare_id = met_info['second_user_id']
    else:
        pare_id = met_info['first_user_id']
    pare_info = get_user_info_by_id(pare_id)
    pare_tg_username = get_tg_username_from_db_by_base_id(pare_id)
    if pare_tg_username:
        pare_username_for_message = f'(@{pare_tg_username})'
    else:
        pare_username_for_message = ''
    if review_info:
        grade = review_info['grade']
        if grade == 0:
            grade_text = 'Встреча не состоялась.'
        else:
            grade_text = f"Оценка - {grade}."
        comment = review_info['comment']
        if comment == 'null':
            comment = 'Не указано'
        review = (
            f"    {grade_text}\n"
            f"    {comment}"
        )
    else:
        review = "A comment on the meeting was not added."

    message = (
        f"<b>Distribution date</b> - {date}.\n"
        f"<b>Your mate</b> – <a href='tg://user?id={pare_info['teleg_id']}'>"
        f"{pare_info['name']}</a> {pare_username_for_message}\n\n"
        f"<b>Review of the meeting:</b>\n"
        f"{review}"

    )
    return message


def get_sqliterow_about_met(met_id):
    """Получаем словарь строки MetInfo."""
    met_info = db_session.query(MetInfo).filter(
        MetInfo.id == met_id
    ).first().__dict__
    return met_info


def get_sqliterow_review(met_id, user_id):
    """Получаем словарь строки Review."""
    try:
        review_info = db_session.query(MetsReview).filter(and_(
            MetsReview.met_id == met_id,
            MetsReview.who_id == user_id
        )).one().__dict__
    except NoResultFound:
        review_info = None
    return review_info


def register_review_history_handler(dp: Dispatcher):
    dp.register_message_handler(get_my_reviews, text=my_reviews)
    dp.register_callback_query_handler(button_press,
                                       review_callbackdata.filter())
