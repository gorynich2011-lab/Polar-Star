#@router.message(Command('goals'))
#async def get_goals(message: Message, state: FSMContext):
#    data = await state.get_data()
#    if data and 'goals' in data:
#        await message.answer(f"Твои цели:\n\n{data['goals']}")
#    else:
#        await message.answer(
#            "У вас пока нет сохраненных целей. Используйте /reg чтобы начать регистрацию.",
#            reply_markup=kb.goals_reg
#        )

#router.message(Command('get_photo'))
#async def get_photo(message: Message):
#    await message.answer_photo(photo='AgACAgIAAxkBAAM3aY9EhryQOISBIQABH5dLIcV3YNjZAALjFWsbnV15SKWp4Lm-u3LVAQADAgADeAADOgQ',
#                               caption='Это фото')


#@router.message(F.photo)
#async def get_photo(message: Message):
#    await message.answer(f'ID фото: {message.photo[-1].file_id}')