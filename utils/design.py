from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_location_keyboard(locations: list[str], row_width: int = 2) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    row = []

    for i, city in enumerate(locations, 1):
        button = InlineKeyboardButton(text=city, callback_data=f"city:{city}")
        row.append(button)

        if i % row_width == 0:
            keyboard.inline_keyboard.append(row)
            row = []

    if row:
        keyboard.inline_keyboard.append(row)

    return keyboard

