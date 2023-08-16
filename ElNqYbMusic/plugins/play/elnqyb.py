import asyncio, random
from pyrogram import Client, filters
from strings import get_command
from strings.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ElNqYbMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from config import OWNER_ID



@app.on_message(filters.command(["الغاء حظر"], "") & filters.group)
async def unbaneed(client, message):
    if not message.reply_to_message: return await message.reply_text(f"**قم بالرد علي رساله**")
    user_id = message.reply_to_message.from_user.id
    try:
        await client.unban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"**تم الغاء حظر هذه المستخدم*")
    except:
         return await message.reply_text(f"**فشل الغاء هذه المستخدم*")
@app.on_message(filters.command(["حظر"], "") & filters.group)
async def baneed(client, message):
    if not message.reply_to_message: return await message.reply_text(f"**قم بالرد علي رساله**")
    user_id = message.reply_to_message.from_user.id
    try:
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply_text(f"**تم حظر هذه المستخدم*")
    except:
         return await message.reply_text(f"**فشل حظر هذه المستخدم*")
mute = []

@app.on_message(filters.command(["كتم"], "") & filters.group)
async def muted(client, message):
    if not message.reply_to_message: return await message.reply_text(f"**قم بالرد علي رساله**")
    user_id = message.reply_to_message.from_user.id
    if not user_id in mute: mute.append(user_id)
    await message.reply_text(f"**تم كتم المستخدم")


@app.on_message(filters.command(["الغاء كتم"], "") & filters.group)
async def muted(client, message):
    if not message.reply_to_message: return await message.reply_text(f"**قم بالرد علي رساله**")
    user_id = message.reply_to_message.from_user.id
    if user_id in mute: mute.remove(user_id)
    await message.reply_text(f"**تم الغاء كتم المستخدم")

@app.on_message(filters.command(["المطور", "مطور"], ""))
async def dev(client: Client, message: Message):
     dev = OWNER_ID[0]
     user = await client.get_chat(chat_id=dev)
     name = user.first_name
     username = user.username 
     bio = user.bio
     user_id = user.id
     photo = user.photo.big_file_id
     photo = await client.download_media(photo)
     link = await client.export_chat_invite_link(message.chat.id)
     title = message.chat.title if message.chat.title else message.chat.first_name
     chat_title = f"User : {message.from_user.mention} \nChat Name : {title}" if message.from_user else f"Chat Name : {message.chat.title}"
     try:
      await client.send_message(username, f"**هناك شخص بالحاجه اليك عزيزي المطور الأساسي**\n{chat_title}\nChat Id : `{message.chat.id}`",
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{title}", url=f"{link}")]]))
     except:
        pass
     await message.reply_photo(
     photo=photo,
     caption=f"**Developer Name : {name}** \n**Devloper Username : @{username}**\n**{bio}**",
     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{name}", user_id=f"{user_id}")]]))

@app.on_message(command(["بوت", "البوت", "اغاني"]))
async def rddd(client, message):
   xx = ["نعم يقلب البوت ♥️🙂", "ضيفني ف جروبك عشان احبك 😂♥️", "معاك يقلبي اتفضل 🙂♥️", "عايز اي مني يعم 😹♥️", "اؤمرني يقلبي 🙂♥️"]
   x = random.choice(xx)
   await message.reply_text(f"**[{x}](https://t.me/{app.username}?startgroup=True)**", disable_web_page_preview=True)


@app.on_message(
     command(["ميمو"])
    & ~filters.edited
)
async def memo(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/28179412acbc52d3873fd.jpg",
caption=f"""**لمراسلة ميمو اضغت علي الزر بالاسفل .**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                
                InlineKeyboardButton(
                    "𝑀é𝓂𝑜𖣩ًََِْٰٓ", url=f"https://t.me/Ankoshhh"
                ),
                ],
                [
                
                InlineKeyboardButton(
                    "قناة السورس", url=f"https://t.me/SOURCETHOR0"
                ),
                ],
            ]
        ),
    )

@app.on_message(
     command(["النقيب", "نقيب", "احمد النقيب"])
    & ~filters.edited
)
async def elnqyb(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/bbda6b6aeb0f63339ace2.jpg",
caption=f"""**لمراسلة احمد النقيب اضغت علي الزر بالاسفل .**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                
                InlineKeyboardButton(
                    "𝗔𝗵𝗠𝗲𝗱 𝗘𝗹𝗡𝗾𝗬𝗯™ ⤶", url=f"https://t.me/pvahmedelnqyb"
                ),
                ],
                [
                
                InlineKeyboardButton(
                    "𝗘𝗹𝗡𝗾𝗬𝗯™★ ⤶", url=f"https://t.me/elnqybch"
                ),
                ],
            ]
        ),
    )


@app.on_message(filters.voice_chat_started)
async def zohary(client: Client, message: Message): 
      await message.reply_text("**تم بدأ محادثع صوتيه .**")

@app.on_message(filters.voice_chat_ended)
async def zoharyy(client: Client, message: Message):
      await message.reply_text("**تم انهاء محادثه صوتيه .**")


@app.on_message(filters.voice_chat_members_invited)
async def fuckoff(client: Client, message: Message):
           text = f"• قام {message.from_user.mention}\n • بدعوة : "
           x = 0
           for user in message.voice_chat_members_invited.users:
               try:
                text += f"{user.mention} "
                x += 1
               except Exception:
                pass
           try:
             await message.reply_text(f"{text} .")
           except:
             pass