#
# Copyright (C) 2021-2022 by TeamElNqYb@Github, < https://github.com/TeamElNqYb >.
#
# This file is part of < https://github.com/TeamElNqYb/ElNqYbMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamElNqYb/ElNqYbMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from config import BANNED_USERS
from ElNqYbMusic import LOGGER, app, userbot
from ElNqYbMusic.core.call import ElNqYb
from ElNqYbMusic.plugins import ALL_MODULES
from ElNqYbMusic.utils.database import get_banned_users, get_gbanned

loop = asyncio.get_event_loop()


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("ElNqYbMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if (
        not config.SPOTIFY_CLIENT_ID
        and not config.SPOTIFY_CLIENT_SECRET
    ):
        LOGGER("ElNqYbMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("ElNqYbMusic.plugins" + all_module)
    LOGGER("ElNqYbmusic.plugins").info(
        "Successfully Imported Modules "
    )
    await userbot.start()
    await ElNqYb.start()
    await ElNqYb.decorators()
    LOGGER("ElNqYbMusic").info("ElNqYb Music Bot Started Successfully")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("ElNqYbMusic").info("Stopping ElNqYb Music Bot! GoodBye")
