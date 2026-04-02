from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.constants import HELP_TEXT, menu_text, premium

import app.keyboards as kb
from app.middlewares import TestMiddleware

router = Router()

router.message.outer_middleware(TestMiddleware())

class Reg(StatesGroup):
    name = State()
    goals = State()
    edit_mode = State()  # состояние для режима редактирования


@router.message(CommandStart())
async def cmd_start_reg(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await state.update_data(is_editing=False)  # Флаг, что это регистрация
    await message.answer(
        f"""
    Привет, {message.from_user.first_name}!
    Мы, Polar Star — поможем тебе с изучением языков.
    Как бы Вы хотели, чтобы мы к Вам обращались?
    Пожалуйста, введите свой никнейм (имя, псевдоним или никнейм)
    """
    )


@router.message(Reg.name)
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    is_editing = data.get('is_editing', False)

    await state.update_data(name=message.text)

    if is_editing:
        await message.answer(
            f'✅ Отлично! Теперь ваш никнейм: {message.text}. Ваш профиль обновлен!',
            reply_markup=kb.down_menu
        )
        await show_updated_profile(message, state)
    else:
        await message.answer(
            f'Приятно познакомиться, {message.text}! Вы можете выбрать действие по кнопочкам снизу, или написать свои цели, почему вы изучаете язык по команде /goals',
            reply_markup=kb.down_menu
        )

    await state.set_state(None)


async def show_updated_profile(message: Message, state: FSMContext):
    """Вспомогательная функция для показа обновленного профиля"""
    data = await state.get_data()
    name = data.get('name')
    goals = data.get('goals')

    if goals:
        await message.answer(
            f"👤 **Обновленный профиль**\n\n"
            f"**Имя:** {name}\n\n"
            f"**Мои цели:**\n{goals}",
            parse_mode='Markdown',
            reply_markup=kb.edit_goals_and_name_keyboard()
        )
    else:
        await message.answer(
            f"👤 **Обновленный профиль**\n\n"
            f"**Имя:** {name}\n\n"
            f"**Цели:** не указаны",
            parse_mode='Markdown',
            reply_markup=kb.edit_name_and_add_goals()
        )


@router.callback_query(F.data == 'edit_nick')
async def edit_nickname(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.set_state(Reg.name)
    await state.update_data(is_editing=True)  # ВАЖНО: сохраняем флаг
    await callback.message.answer("Введите новый никнейм:")


@router.message(Command('goals'))
async def goals_get(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data or 'name' not in data:
        await message.answer(
            "Сначала нужно зарегистрироваться! Используйте /start"
        )
        return

    await state.set_state(Reg.goals)
    await message.answer('Какие у Вас цели на изучение языка?')


@router.message(Reg.goals)
async def goals_name(message: Message, state: FSMContext):
    await state.update_data(goals=message.text)
    await message.answer(
        'Успешно! Теперь посмотреть или изменить цели можно в профиле. Удачи с изучением языка!',
        reply_markup=kb.down_menu
    )
    await state.set_state(None)


@router.message(F.text == 'Мой профиль')
@router.message(Command('profile'))
async def get_profile(message: Message, state: FSMContext):
    data = await state.get_data()

    name = data.get('name')
    if not name:
        await message.answer(
            "❌ Что-то пошло не так. Пожалуйста, пройдите регистрацию заново:\n/start",
            reply_markup=kb.down_menu
        )
        return

    goals = data.get('goals')

    if goals:
        await message.answer(
            f"👤 **Мой профиль**\n\n"
            f"**Имя:** {name}\n\n"
            f"**Мои цели:**\n{goals}",
            parse_mode='Markdown',
            reply_markup=kb.edit_goals_and_name_keyboard()
        )
    else:
        await message.answer(
            f"👤 **Мой профиль**\n\n"
            f"**Имя:** {name}\n\n"
            f"**Цели:** не указаны\n\n"
            f"Чтобы добавить цели, нажмите кнопку ниже:",
            parse_mode='Markdown',
            reply_markup=kb.edit_name_and_add_goals()
        )


@router.callback_query(F.data == 'add_goals')
async def add_goals(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.set_state(Reg.goals)
    await callback.message.answer("Введите ваши цели:")


@router.callback_query(F.data == 'edit_goals')
async def edit_goals(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.set_state(Reg.goals)
    await callback.message.answer("Введите новые цели:")


@router.message(F.text == 'Помощь')
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer(HELP_TEXT, parse_mode='Markdown', reply_markup=kb.main)


@router.message(F.text == 'Главное меню')
@router.message(Command('menu'))
async def get_menu(message: Message):
    await message.answer(
        menu_text,
        parse_mode='Markdown',
        reply_markup=kb.main
    )


@router.callback_query(F.data == 'start_lesson')
async def start_lesson(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Отлично! Давай начнем. На какую тему ты хоче заниматься?',
        reply_markup=kb.back_options
    )


@router.callback_query(F.data == 'exams')
async def exams_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Режим подготовки к экзаменам. Какой тебя интересует?',
        reply_markup=kb.back_options
    )


@router.callback_query(F.data == 'career')
async def career_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Режим изучения языка для карьеры и других целей. Выбери направление: IT, Бизнес или медицина.',
        reply_markup=kb.back_options
    )


@router.message(Command('premium'))
async def get_premium(message: Message):
    await message.answer(premium, parse_mode='Markdown')


@router.callback_query(F.data == 'premium')
async def premium_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(premium, parse_mode='Markdown', reply_markup=kb.back_options)


@router.callback_query(F.data == 'results')
async def results_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Твой прогресс: ...',
        reply_markup=kb.back_options
    )


@router.message(Command('results'))
async def get_results(message: Message):
    await message.answer('Твой прогресс: ...', reply_markup=kb.back_options)


@router.callback_query(F.data == 'contacts')
async def contacts_handler(callback: CallbackQuery):
    await callback.answer()

    email = "hipolarstar@mail.ru"

    text = f"""
💬 Если у вас есть вопросы, пишите на почту — ответим в ближайшее время!
Наши соцсети:

📧 **Email:** [{email}](mailto:{email})
"""

    await callback.message.edit_text(
        text=text,
        parse_mode='Markdown',
        reply_markup=kb.get_contact_keyboard()
    )


@router.callback_query(F.data == 'back')
async def back_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        menu_text,
        parse_mode='Markdown',
        reply_markup=kb.main
    )