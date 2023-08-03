from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from controllerBD.db_loader import db_session
from controllerBD.models import Gender, Users, UserStatus, UserMets, Holidays
from handlers.admin.ban_handlers import back_to_main_markup
from handlers.user.add_username import check_username
from handlers.user.first_check import check_and_add_registration_button
from handlers.user.get_info_from_table import (
    check_user_in_base,
    get_id_from_user_info_table
)
from handlers.user.work_with_date import date_from_message_to_db
from keyboards.user import (back_message, confirm_markup,
                            man_message, register_can_skip_reply_markup,
                            register_man_or_woman_markup,
                            skip_message, woman_message,
                            return_to_begin_button, registr_message,
                            return_to_begin_markup)
from loader import bot, logger
from states.states import UserData

from handlers.user.validators import (validate_about, validate_birthday,
                                      validate_check_info, validate_gender,
                                      validate_name)


# @dp.message_handler(text=return_to_begin_button, state="*")
async def return_to_begin(message: types.Message, state: FSMContext):
    """Вывод меню"""
    await state.reset_state()
    await check_and_add_registration_button(message)


def get_gender_from_db(status):
    """Получаем пол пользователя по id пола"""
    info = db_session.query(Gender.gender_name).filter(
        Gender.id == status
    ).first()
    return info[0]


# @dp.message_handler(state=UserData.check_info)
async def confirmation_and_save(message: types.Message, state: FSMContext):
    """Подтверждение пользователем введенных данных"""
    if not await validate_check_info(message):
        return
    answer = message.text
    if answer == back_message:
        await question_gender(message)
    else:
        await bot.send_message(
            message.from_user.id,
            'Hurrah! Now you are participating in the distribution next week. '
            'The bot will remind you: before the distribution, a message will come that '
            "they'll pick up a pair for you soon.",
            reply_markup=ReplyKeyboardRemove()
        )
        await bot.send_message(
            message.from_user.id,
            text="Use the menu",
            reply_markup=back_to_main_markup(message),
        )
        data = await state.get_data()
        if await check_user_in_base(message):
            update_profile_db(message.from_user.id,
                              data.get('name'),
                              data.get('birthday'),
                              data.get('about'),
                              data.get('gender'))
        else:
            add_to_db(message.from_user.id,
                      data.get('name'),
                      data.get('birthday'),
                      data.get('about'),
                      data.get('gender'))
            await add_new_user_in_status_table(message)
        await state.reset_state()


async def change_data(message: types.Message, state: FSMContext):
    """Отправка пользователя на повторное прохождение регистрации"""
    await state.reset_state()
    await start_registration(message)


def add_to_db(teleg_id, name, birthday, about, gender):
    """Добавляем нового пользователя в базу."""
    if birthday == "Не указано":
        pass
    else:
        birthday = date_from_message_to_db(birthday)
    db_session.add(Users(teleg_id=teleg_id, name=name,
                         birthday=birthday, about=about, gender=gender))
    db_session.commit()
    logger.info(f"Пользователь с TG_ID {teleg_id} "
                f"добавлен в БД как новый участник")


def update_profile_db(teleg_id, name, birthday, about, gender):
    """Обновление данных пользователя"""
    if birthday == "Не указано":
        pass
    else:
        birthday = date_from_message_to_db(birthday)
    db_session.query(Users).filter(Users.teleg_id == teleg_id). \
        update({'name': name, 'birthday': birthday,
                'about': about, 'gender': gender})
    db_session.commit()
    logger.info(f"Пользователь с TG_ID {teleg_id} "
                f"обновил информацию о себе")


async def add_new_user_in_status_table(message):
    """Проставляем статусы участия в таблицах БД"""
    user_id = get_id_from_user_info_table(message.from_user.id)
    db_session.add(UserStatus(id=user_id))
    db_session.commit()
    db_session.add(UserMets(id=user_id))
    db_session.commit()
    db_session.add(Holidays(id=user_id))
    db_session.commit()
    await check_username(message)


# @dp.message_handler(text=registr_message, state=UserData.start)
async def start_registration(message: types.Message):
    """Первое состояние. Старт регистрации."""
    logger.info(f"User with TG_ID {message.from_user.id} "
                f"started the registration process")
    await bot.send_message(
        message.from_user.id,
        'How do I introduce you to the buddy? (Enter only the name)',
        reply_markup=return_to_begin_markup()
    )
    await UserData.name.set()


async def check_data(tg_id, name, birthday, about, gender):
    """Вывод данных пользователя для проверки"""
    await bot.send_message(
        tg_id,
        f"This card will be seen by your interlocutor during the distribution:\n\n"
        f"Name: {name}\n"
        f"Birthday: {birthday}\n"
        f"About me: {about}\n"
        f"Sex: {gender}\n\n"
        f"Is that right?",
        reply_markup=confirm_markup()
    )
    await UserData.check_info.set()


async def end_registration(state, message):
    """Формирование данных пользователя для проверки"""
    data = await state.get_data()
    name = data.get('name')
    birthday = data.get('birthday')
    about = data.get('about')
    gender = get_gender_from_db(data.get('gender'))
    tg_id = message.from_user.id
    await check_data(tg_id, name, birthday, about, gender)


# @dp.message_handler(state=UserData.name)
async def answer_name(message: types.Message, state: FSMContext):
    """Второе состояние. Сохранение имени в хранилище памяти."""
    name = message.text
    if not validate_name(name):
        await message.answer(
            'Something is wrong with the name you entered. '
            'The name must consist of letters of the Russian or Latin alphabets '
            'and be less than 100 characters.'
        )
        return
    await state.update_data(name=name)
    await question_birthday(message)


async def question_birthday(message: types.Message):
    """Запрос даты рождения"""
    await bot.send_message(
        message.from_user.id,
        'Please enter your date of birth in the format DD.MM.YYYY',
        reply_markup=register_can_skip_reply_markup()
    )
    await UserData.birthday.set()


# @dp.message_handler(state=UserData.birthday)
async def answer_birthday(message: types.Message, state: FSMContext):
    """Третье состояние. Сохранение даты рождения в хранилище памяти."""
    birthday = message.text
    if birthday == back_message:
        await start_registration(message)
    else:
        if birthday == skip_message:
            birthday = 'Not specified'
        else:
            if not await validate_birthday(message):
                return
        await state.update_data(birthday=birthday)
        await question_about(message)


async def question_about(message: types.Message):
    """Запрос информации о пользователе"""
    await bot.send_message(
        message.from_user.id,
        "Tell me a little about yourself?",
        reply_markup=register_can_skip_reply_markup()
    )
    await UserData.about.set()


# @dp.message_handler(state=UserData.about)
async def answer_about(message: types.Message, state: FSMContext):
    """Четвертое состояние.
    Сохранение информации о пользователе в хранилище памяти."""
    about = message.text
    if about == back_message:
        await question_birthday(message)
    else:
        if about == skip_message:
            about = 'Not specified'
        else:
            if not await validate_about(message):
                return
        await state.update_data(about=about)
        await question_gender(message)


async def question_gender(message: types.Message):
    """Запрос пола пользователя"""
    await bot.send_message(
        message.from_user.id,
        "Choose a gender",
        reply_markup=register_man_or_woman_markup()
    )
    await UserData.gender.set()


# @dp.message_handler(state=UserData.gender)
async def answer_gender(message: types.Message, state: FSMContext):
    """Пятое состояние. Сохранение гендера в хранилище памяти."""
    gender = message.text
    if gender == back_message:
        await question_about(message)
    else:
        if not await validate_gender(message):
            return
        elif gender == skip_message:
            gender = 0
        elif gender == woman_message:
            gender = 1
        elif gender == man_message:
            gender = 2
        await state.update_data(gender=gender)
        await end_registration(state, message)


def register_new_member_handler(dp: Dispatcher):
    dp.register_message_handler(return_to_begin, text=return_to_begin_button,
                                state="*")
    dp.register_message_handler(confirmation_and_save,
                                state=UserData.check_info)
    dp.register_message_handler(start_registration, text=registr_message,
                                state=UserData.start)
    dp.register_message_handler(answer_name, state=UserData.name)
    dp.register_message_handler(answer_birthday, state=UserData.birthday)
    dp.register_message_handler(answer_about, state=UserData.about)
    dp.register_message_handler(answer_gender, state=UserData.gender)
