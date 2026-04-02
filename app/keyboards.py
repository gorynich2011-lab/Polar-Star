from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    ForceReply
)
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder  # Вот это нужно импортировать отсюда
)

# Reply-клавиатура (нижняя)
down_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Главное меню"), KeyboardButton(text="Мой профиль")],
        [KeyboardButton(text="Настройки"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)


def edit_name_and_add_goals():
    """Клавиатура для профиля без целей"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Изменить никнейм', callback_data='edit_nick'),
        InlineKeyboardButton(text='Добавить цели', callback_data='add_goals')
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Главное меню", callback_data="back")
    )
    return builder.as_markup()


def edit_goals_and_name_keyboard():
    """Клавиатура для профиля с целями"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text='Изменить никнейм', callback_data='edit_nick'),
        InlineKeyboardButton(text="Изменить цели", callback_data='edit_goals')
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Главное меню", callback_data="back")
    )
    return builder.as_markup()


def get_contact_keyboard():
    """Клавиатура для контактов"""
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(text="📺 YouTube", url="https://youtube.com/@PolarStarAi"),
        InlineKeyboardButton(text="🎵 TikTok", url="https://www.tiktok.com/@polar.star96")
    )

    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="back")
    )

    return builder.as_markup()


def get_back_options():
    """Клавиатура только с кнопкой назад"""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="back")
    )
    return builder.as_markup()


# Готовые экземпляры клавиатур
back_options = get_back_options()

# Главная inline-клавиатура
main = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="📚 Начать урок", callback_data="start_lesson"),
            InlineKeyboardButton(text="🎯 Hylget", callback_data="exams")
        ],
        [
            InlineKeyboardButton(text="💼 Primar", callback_data="career"),
            InlineKeyboardButton(text="⭐️ Premium", callback_data="premium")
        ],
        [
            InlineKeyboardButton(text="📊 Результаты", callback_data="results"),
            InlineKeyboardButton(text="ℹ️ Больше о нас", callback_data="contacts")
        ]
    ]
)