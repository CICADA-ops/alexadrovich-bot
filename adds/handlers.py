class States(StatesGroup):
    photo = State()


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer('Привет! Тут потом будет текст для представления, '
                         'а пока, выбери что хочешь сделать)', reply_markup=kb.menu_keyboard)


@router.message(F.text == "Конвертер")
async def converter_button(message: Message, state: FSMContext) -> None:
    #await state.set_state(States.photo)
    await message.answer("Пришли мне фото (файлом!)")

'''
@router.message(States.photo, F.document)
async def handle_document(message: Message) -> None:
    file_id = message.document.file_id
    filename = await download_file(file_id)
    if filename:

        await message.answer(f"Файл '{filename}' успешно скачан.")
    else:
        await message.answer("Произошла ошибка при скачивании файла. Попробуйте снова")

'''
@router.message(F.document)
async def handle_document(message: Message) -> None:
    file_id = message.document.file_id
    filename = await download_file(file_id)
    if filename:
        await message.answer(f"Файл '{filename}' успешно скачан.")
    else:
        await message.answer("Произошла ошибка при скачивании файла.")

