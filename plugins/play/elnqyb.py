import asyncio, random
from pyrogram import Client, filters
from strings import get_command
from strings.filters import command
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from ElNqYbMusic import (Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app)
from config import OWNER_ID


id = {}
@app.on_callback_query(filters.regex("heart"))  
async def heart(client, query: CallbackQuery):  
    callback_data = query.data.strip()  
    callback_request = callback_data.replace("heart", "")  
    username = int(callback_request)
    usr = await client.get_chat(username)
    if not query.from_user.mention in id[usr.id]:
         id[usr.id].append(query.from_user.mention)
    else:
         id[usr.id].remove(query.from_user.mention)
    idd = len(id[usr.id])
    await query.edit_message_text(f"**NAME : {usr.first_name}**\n**BIO : {usr.bio} .", reply_markup=InlineKeyboardMarkup(  
            [
                [ 
                    InlineKeyboardButton(  
                        f"يوزرك", callback_data=f"usernamec{usr.id}")
                ],
                [  
                    InlineKeyboardButton(  
                        f"ايديك", callback_data=f"idc{usr.id}")
                ],
                [  
                    InlineKeyboardButton(  
                        f"♥️ {idd}", callback_data=f"heart{usr.id}")
                ],  
            ]  
        ),  
    )
@app.on_callback_query(filters.regex("idc"))  
async def xxid(client, query: CallbackQuery):  
    callback_data = query.data.strip()  
    callback_request = callback_data.replace("idc", "")  
    username = int(callback_request) 
    if not query.from_user.id == username: 
       return await query.answer("لايمكنك طباعه معلومات شخص اخر : ❤️", show_alert=True) 
    username = f"ايديك هو : `{username}`" if username else "ليس لديك ايدي" 
    await query.message.reply_to_message.reply_text(username)  

@app.on_callback_query(filters.regex("usernamec"))  
async def xxuser(client, query: CallbackQuery):  
    callback_data = query.data.strip()  
    callback_request = callback_data.replace("usernamec", "")  
    username = int(callback_request) 
    if not query.from_user.id == username: 
       return await query.answer("لايمكنك طباعه معلومات شخص اخر : ❤️", show_alert=True) 
    user = await client.get_chat(username) 
    username = f"معرفك هو : @{user.username}" if user.username else "ليس لديك معرف" 
    await query.message.reply_to_message.reply_text(username)  

@app.on_message(  
    filters.command(["ايدي", "ا"], "")  
)  
async def ssorh(client, message):  
    usr = await client.get_chat(message.from_user.id)  
    name = usr.first_name
    if not id.get(message.from_user.id):
       id[usr.id] = []
    idd = len(id[usr.id])
    await client.send_photo(message.chat.id, photo="https://telegra.ph/file/d3d23e8cff24c7c1df1fe.jpg", caption=f"**NAME : {message.from_user.first_name}**\n**BIO : {usr.bio}", reply_to_message_id=message.message_id,  
    reply_markup=InlineKeyboardMarkup(  
            [
                [ 
                    InlineKeyboardButton(  
                        f"يوزرك", callback_data=f"usernamec{usr.id}")
                ],
                [  
                    InlineKeyboardButton(  
                        f"ايديك", callback_data=f"idc{usr.id}")
                ],
                [  
                    InlineKeyboardButton(  
                        f"♥️ {idd}", callback_data=f"heart{usr.id}")
                ],
            ]  
        ),  
    )

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
    if user_id in mute: mute.append(user_id)
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
        photo=f"https://telegra.ph/file/bbda6b6aeb0f63339ace2.jpg",
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