from aiogram.types import ReplyKeyboardMarkup

from data import ADMIN_TG_ID

back_message = '👈 Back'
skip_message = '👉 Skip'
all_right_message = "✅ That's right"
cancel_message = '🚫 Cancel'
menu_message = '🏠 Menu'
confirm_message = '✅ Yes'
reject_message = '❌ No'
edit_profile_message = "👩🏿‍🎨 Change Profile"
my_profile_message = "My profile"
my_status_message = "My status"
my_reviews = "My meetings"
set_holiday_message = "⛱️ holidays"
about_bot_message = "🤖 About/FAQ"
man_message = "👨 Male"
woman_message = "👩 Female"
registr_message = "Register"
return_to_begin_button = "Go back to the beginning"
help_texts = "Where to start"
one_week_holidays_message = "1 week"
two_week_holidays_message = "2 weeks"
three_week_holidays_message = "3 weeks"
turn_off_holidays = "turn off"
back_to_menu = "Go back to the menu"
my_pare_button = "My peer"
back_to_main = 'Main page'


def main_markup():
    """Главная клавиатура."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(menu_message)

    return markup


def menu_markup(message):
    """Клавиатура главного меню."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(my_profile_message, my_pare_button)
    markup.row(my_status_message, set_holiday_message)
    markup.row(about_bot_message, my_reviews)
    if message.from_user.id in list(map(int, ADMIN_TG_ID.split())):
        markup.row(back_to_main)

    return markup


def edit_profile_markup():
    """Клавиатура редактирование профиля."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(edit_profile_message)
    markup.row(back_to_menu)
    return markup


def confirm_markup():
    """Клавиатура подтверждения."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(all_right_message)
    markup.add(back_message, return_to_begin_button)
    return markup


def return_to_begin_markup():
    """Клавиатура подтверждения."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(return_to_begin_button)
    return markup


def start_registr_markup():
    """Клавиатура начала регистрации."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(registr_message)

    return markup


def register_can_skip_reply_markup():
    """Клавиатура назад-пропустить"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(back_message, skip_message)
    markup.row(return_to_begin_button)

    return markup


def register_reply_markup():
    """Кнопка назад."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(back_message, return_to_begin_button)

    return markup


def register_man_or_woman_markup():
    """Клавиатура выбора пола."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(man_message, woman_message)
    markup.row(back_message, skip_message)
    markup.row(return_to_begin_button)

    return markup


def holidays_length():
    """Выбор длины каникул."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(one_week_holidays_message, two_week_holidays_message)
    markup.row(three_week_holidays_message, turn_off_holidays)
    markup.row(back_to_menu)
    return markup


def help_texts_markup():
    """Клавиатура с чего начать разговор."""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.row(help_texts)
    markup.row(return_to_begin_button)
    return markup
