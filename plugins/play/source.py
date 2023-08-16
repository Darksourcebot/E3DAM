from pyrogram import Client, filters
from strings.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from ElNqYbMusic import app

@app.on_message(
    command(["سورس","السورس"])
    & ~filters.edited
)
async def khalid(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("𝙶𝚁𝙾𝚄𝙿️", url=f"https://t.me/"),
                InlineKeyboardButton("𝚂𝙾𝚄𝚁𝙲𝙴️", url=f"https://t.me/"),
            ],
            [
                 InlineKeyboardButton(f"", url=f"https://t.me/")
            ]
        ]
    )

    await message.reply_photo(
        photo="",
        caption="",
        reply_markup=keyboard,
    )