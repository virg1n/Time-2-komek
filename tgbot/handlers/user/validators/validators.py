import re
from datetime import datetime

from aiogram import types
from keyboards.user import (all_right_message, back_message, man_message,
                            skip_message, woman_message, yes_button, no_button)
from loader import bot


def validate_name(message):
    """Валидация введенных данных в поле Имя"""
    return (re.fullmatch(
        r"^[a-яА-ЯЁёa-zA-Z\s]{1,100}$",
        message
    ) and len(message) <= 100)


async def validate_birthday(message: types.Message):
    """Валидация введенных данных в поле Дата рождения"""
    if re.fullmatch(
        r"^((0[1-9]|[12]\d)\.(0[1-9]|1[012])|"
        r"30\.(0[13-9]|1[012])|31\.(0[13578]|1[02]))\.(19|20)\d\d$",
        message.text
    ):
        date_obj = datetime.strptime(message.text, '%d.%m.%Y')
        difference = datetime.now() - date_obj
        age = int(difference.days) / 365.2
        if age < 0:
            await bot.send_message(
                message.from_user.id,
                'A date from the future?)) Enter the correct date of birth'
            )
            return False
        elif age <= 14:
            await bot.send_message(
                message.from_user.id,
                'Your age must be over 14 years old. '
                'Enter the correct date of birth'
            )
            return False
        elif age > 120:
            await bot.send_message(
                message.from_user.id,
                'The specified age is more than 120 years old.'
                'Enter the correct date of birth'
            )
            return False
        return True
    await bot.send_message(
        message.from_user.id,
        'Something is wrong with the entered data.'
        'The date must consist of digits and dots in the format DD.MM.YYYY'
    )
    return False


async def validate_about(message):
    """Валидация введенных данных в поле О себе"""
    if len(message.text) > 500:
        await bot.send_message(
            message.from_user.id,
            'The text must be less than 500 characters. Repeat the input.'
        )
        return False
    elif not re.fullmatch(r"^[^<>]+$", message.text):
        await bot.send_message(
            message.from_user.id,
            'It is forbidden to use <> characters in the text. Repeat the input.'
        )
        return False
    return True


async def validate_gender(message: types.Message):
    """Валидация введенных данных в поле Пол пользователя"""
    choice = [man_message, woman_message, skip_message]
    if message.text not in choice:
        await bot.send_message(
            message.from_user.id,
            'Please choose from the available options or '
            'click "Skip"'
        )
        return False
    return True


async def validate_check_info(message):
    """Валидация введенных данных при проверке выбора
    в форме подтверждения введенных данных"""
    choice = [all_right_message, back_message]
    if message.text not in choice:
        await bot.send_message(
            message.from_user.id,
            'Please choose from the available options.'
        )
        return False
    return True


async def validate_review_yes_or_no(message):
    choice = [yes_button, no_button, skip_message]
    if message.text not in choice:
        await bot.send_message(
            message.from_user.id,
            'Please choose from the available options.'
        )
        return False
    return True


async def validate_review_grade(grade):
    return re.fullmatch(r"^[1-5]{1,1}$", grade)
