#
# Copyright (C) 2021-2022 by TeamElNqYb@Github, < https://github.com/TeamElNqYb >.
#
# This file is part of < https://github.com/TeamElNqYb/ElNqYbMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamElNqYb/ElNqYbMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from strings.filters import command
from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from ElNqYbMusic import app
from ElNqYbMusic.core.call import ElNqYb
from ElNqYbMusic.utils.database import set_loop
from ElNqYbMusic.utils.decorators import AdminRightsCheck

# Commands
STOP_COMMAND = get_command("STOP_COMMAND")


@app.on_message(
    command(STOP_COMMAND)
    & filters.group
)
@AdminRightsCheck
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    await ElNqYb.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        _["admin_9"].format(message.from_user.mention)
    )


@app.on_message(
    command(STOP_COMMAND)
    & filters.channel
    & ~filters.edited
)
async def stopmusic(client, message):
    if not len(message.command) == 1:
        return
    chat_id = message.chat.id
    await ElNqYb.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text("تم انهاء التشغيل .")
