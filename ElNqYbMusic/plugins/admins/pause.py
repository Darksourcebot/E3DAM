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
from strings import get_string
from config import BANNED_USERS
from strings import get_command
from ElNqYbMusic import app
from ElNqYbMusic.core.call import ElNqYb
from ElNqYbMusic.utils.database import is_music_playing, music_off
from ElNqYbMusic.utils.decorators import AdminRightsCheck

# Commands
PAUSE_COMMAND = get_command("PAUSE_COMMAND")


@app.on_message(
    command(PAUSE_COMMAND)
    & filters.group
)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await ElNqYb.pause_stream(chat_id)
    await message.reply_text(
        _["admin_2"].format(message.from_user.mention)
    )
    
    
    
@app.on_message(
    command(PAUSE_COMMAND)
    & filters.channel
)
async def pauseadmin(cli, message):
    _ = get_string("en")
    chat_id = message.chat.id
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if not await is_music_playing(chat_id):
        return await message.reply_text(_["admin_1"])
    await music_off(chat_id)
    await ElNqYb.pause_stream(chat_id)
    await message.reply_text(
        _["admin_2"].format(message.chat.title)
    )
