import asyncio
import requests, re
from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)
from youtubesearchpython.__future__ import VideosSearch

import config, re
from config import BANNED_USERS
from config.config import OWNER_ID
from strings import get_command, get_string
from ElNqYbMusic import Telegram, YouTube, app
from ElNqYbMusic.misc import SUDOERS
from ElNqYbMusic.misc import SUDOERS as sudo
from ElNqYbMusic.plugins.play.playlist import del_plist_msg
from ElNqYbMusic.plugins.play.elnqyb import mute, words, links
from ElNqYbMusic.utils.database import (add_served_chat,
                                       is_served_chat,
                                       get_served_chats,
                                       add_served_user,
                                       get_served_users,
                                       blacklisted_chats,
                                       get_assistant, get_lang,
                                       get_userss, is_on_off,
                                       is_served_private_chat,
                                       is_active_chat)
from ElNqYbMusic.utils.decorators.language import LanguageStart
from ElNqYbMusic.utils.inline import (help_pannel, private_panel,
                                     start_pannel)
from ElNqYbMusic import joinch

loop = asyncio.get_running_loop()


@app.on_message(
    filters.command(get_command("START_COMMAND"))
    & filters.private
    & ~filters.edited
    & ~BANNED_USERS
)
@LanguageStart
async def start_comm(client, message: Message, _):
    if await joinch(message): return
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            return await message.reply_text(
                _["help_1"], reply_markup=keyboard
            )
        if name[0:4] == "song":
            return await message.reply_text(_["song_2"])
        if name[0:3] == "sta":
            m = await message.reply_text(
                "🔎 Fetching your personal stats.!"
            )
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"🔗[Telegram Files and Audios](https://t.me/telegram) ** played {count} times**\n\n"
                    else:
                        msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) ** played {count} times**\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(
                    None, get_stats
                )
            except Exception as e:
                print(e)
                return
            thumbnail = await YouTube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"**• دخول مستخدم جديد للبوت 🤖**\n**•ايدي المستخدم ->** {sender_id}\n**• اسم المستخدم -> ** {message.from_user.mention}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                return await Telegram.send_split_text(message, lyrics)
            else:
                return await message.reply_text(
                    "Failed to get lyrics."
                )
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 Fetching Info!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[
                    0
                ]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🔍__**Video Track Information**__

❇️**Title:** {title}

⏳**Duration:** {duration} Mins
👀**Views:** `{views}`
⏰**Published Time:** {published}
🎥**Channel Name:** {channel}
📎**Channel Link:** [Visit From Here]({channellink})
🔗**Video Link:** [Link]({link})

⚡️ __Searched Powered By {config.MUSIC_BOT_NAME}__"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 Watch ", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="🔄 Close", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} has just started bot to check <code>VIDEO INFORMATION</code>\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}",
                )
    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        out = private_panel(_, app.username, OWNER)
        if config.START_IMG_URL:
            try:
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_2"].format(
                        config.MUSIC_BOT_NAME
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            except:
                await message.reply_text(
                    _["start_2"].format(config.MUSIC_BOT_NAME),
                    reply_markup=InlineKeyboardMarkup(out),
                )
        else:
            await message.reply_text(
                _["start_2"].format(config.MUSIC_BOT_NAME),
                reply_markup=InlineKeyboardMarkup(out),
            )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} has just started Bot.\n\n**USER ID:** {sender_id}\n**USER NAME:** {sender_name}",
            )


@app.on_message(
    filters.command(get_command("START_COMMAND"))
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@LanguageStart
async def testbot(client, message: Message, _):
    out = start_pannel(_)
    return await message.reply_text(
        _["start_1"].format(
            message.chat.title, config.MUSIC_BOT_NAME
        ),
        reply_markup=InlineKeyboardMarkup(out),
    )


welcome_group = 2


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(client, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                "**Private Music Bot**\n\nOnly for authorized chats from the owner. Ask my owner to allow your chat first."
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                if chat_type != "supergroup":
                    await message.reply_text(_["start_6"])
                    return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_7"].format(
                            f"https://t.me/{app.username}?start=sudolist"
                        )
                    )
                    return await app.leave_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    _["start_3"].format(
                        config.MUSIC_BOT_NAME,
                        userbot.username,
                        userbot.id,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_4"].format(
                        config.MUSIC_BOT_NAME, member.mention
                    )
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_5"].format(
                        config.MUSIC_BOT_NAME, member.mention
                    )
                )
            return
        except:
            return
def linkcheck(text):
  list = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s!()\[\]{};:'\".,<>?«»“”‘’]))"
  url = re.findall(list,text)
  return [x[0] for x in url]
def wordscheck(text):
  list = "كسم|خول|علق|علء|كثم|متناك|عرص|عرث|خخخ|لبوه|لبوة|زبر|طيز|fuck|xnxx|porn|six|احا|خخخ"
  txt = text.replace(".", "")
  words = re.findall(list,txt)
  return words
smsm = []
url = "https://bumcomingo.simsimi.com/simtalk/get_talk_set"
headers = {'accept': 'application/json, text/plain, */*','os': 'a','av': '8.4.4','appcheck': '','Content-Type': 'application/json','Content-Length': '159','Host': 'bumcomingo.simsimi.com','Connection': 'Keep-Alive','Accept-Encoding': 'gzip','User-Agent': 'okhttp/4.9.1'}
@app.on_message(filters.command(["تفعيل الرد"], "") & filters.group)
async def smsmon(client, message):
    if not message.from_user.id in sudo:
     chek = await client.get_chat_member(message.chat.id, message.from_user.id)
     if not chek.status in ["administrator", "creator"] : return await message.reply_text(f"**لا يمكنك تنفيذ هذا الامر**")
    if not message.chat.id in smsm:
        smsm.append(message.chat.id)
    await message.reply_text(f"**تم تفعيل الرد بنجاح**")
@app.on_message(filters.command(["تعطيل الرد"], "") & filters.group)
async def smsmof(client, message):
    if not message.from_user.id in sudo:
     chek = await client.get_chat_member(message.chat.id, message.from_user.id)
     if not chek.status in ["administrator", "creator"] : return await message.reply_text(f"**لا يمكنك تنفيذ هذا الامر**")
    if message.chat.id in smsm:
        smsm.remove(message.chat.id)
    await message.reply_text(f"**تم تعطيل الرد بنجاح**")
@app.on_message(~filters.private)       
async def autopmPermiat(client, message: Message):
    chat_id = message.chat.id
    if message.from_user:
       if message.from_user.id in mute:
          return await message.delete()
    if not await is_served_chat(chat_id):
        await add_served_chat(chat_id)
    if "Code" in message.text:
        text = message.text.split("Code: ")[1]
        if " " in text:
           text = text.split(" ")[0]
        await message.reply_text(f"`{text}`")
    if linkcheck(str(message.text)) and message.chat.id in links: await message.delete()
    if wordscheck(str(message.text)) and message.chat.id in words: await message.delete()
    text = message.text
    if text == "خاص": await message.reply_text("عيب")
    if text == "كسبت": await message.reply_text("يافلوسك")
    if text == "كود": await message.reply_text("انت بوت")
    if text == "انا مين": await message.reply_text("معرفكش")
    if text == "حبيبتي": await message.reply_text("طيب و انا")
    if text == "بوت": await message.reply_text("هنكد عليك")
    if text == "خسرنا": await message.reply_text("احسن")
    if text == "قول اسف": await message.reply_text("اللعب بعيد")
    if text == "هات كود": await message.reply_text("مليش مزاج")
    if text == "قلبى": await message.reply_text("و ايه كمان")
    if text == "فارس": await message.reply_text("حبيبي انا")
    if text == "هلال": await message.reply_text("ده قلبي ده")
    if text == "ممكن دعم": await message.reply_text("محدش هنا لاقي ياكل")
    if text == "الاوامر": await message.reply_text("""كتم -الغاء كتم
تقيد -الغاء تقيد
حظر -الغاء حظر
منع الاسائه -فتح الاسائه
منع الروابط -فتح الروابط""")
    if message.chat.id in smsm:
     if message.from_user.is_self: return
     payload = {"uid": 414477568,"av": "8.4.4","os": "a","lc": "ar","cc": "EG","tz": "Africa/Cairo","cv": "","message": text,"free_level": 1,"logUID": "414477568","reg_now_days": 0}
     response = requests.post(url, json=payload, headers=headers)
     try:
      out = response.json()['sentence']
     except:
        out = response.json()['detail']
     out = re.sub('@[a-zA-Z]{3,}', '،', out)
     out = re.sub(r'[0-9]+', '', out)
     await message.reply_text(out)
    message.continue_propagation()



@app.on_message(filters.command(["الاحصائيات", "احصائيات"], "") & SUDOERS)
async def analysis(client, message: Message):
   chats = len(await get_served_chats())
   user = len(await get_served_users())
   await message.reply_text(f"**✅ احصائيات البوت**\n**⚡ المجموعات {chats} مجموعة  **\n**⚡ المستخدمين {user} مستخدم**")
