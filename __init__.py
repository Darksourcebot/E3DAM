#
# Copyright (C) 2021-2022 by TeamElNqYb@Github, < https://github.com/TeamElNqYb >.
#
# This file is part of < https://github.com/TeamElNqYb/ElNqYbMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamElNqYb/ElNqYbMusicBot/blob/master/LICENSE >
#
# All rights reserved.

from ElNqYbMusic.core.bot import ElNqYbBot
from ElNqYbMusic.core.dir import dirr
from ElNqYbMusic.core.git import git
from ElNqYbMusic.core.userbot import Userbot
from ElNqYbMusic.misc import dbb, heroku, sudo
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from .logging import LOGGER

# Directories
dirr()

# Check Git Updates
git()

# Initialize Memory DB
dbb()

# Heroku APP
heroku()

# Load Sudo Users from DB
sudo()

# Bot Client
app = ElNqYbBot()

# Assistant Client
userbot = Userbot()

from .platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Apple = AppleAPI()
Resso = RessoAPI()
SoundCloud = SoundAPI()
Telegram = TeleAPI()

async def joinch(message):
    if not message.from_user: return
    try:
            await message._client.get_chat_member("SOURCETHOR0", message.from_user.id)
    except UserNotParticipant:
                await message.reply(
                    f"🚦 يجب ان تشترك في القناة\n\nقنـاة الـبـوت : « https://t.me/SOURCETHOR0 »",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("اضـغط هنا للأشتـراك القنـاة 🚦", url=f"https://t.me/SOURCETHOR0"),
                            ],
                         ] 
                      ) 
                   )
                return True
    except:
        pass