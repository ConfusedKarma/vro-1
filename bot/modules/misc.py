from bot import vro

CUSTOM_CMD = ["/", "!"]


import os

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.helper import http
from json import loads as json_loads
from os import remove
from re import compile as compiles

# View Structure Telegram Message As JSON
@vro.on_message(filters.command(["json"], CUSTOM_CMD))
async def jsonify(_, message):
    the_real_message = None
    reply_to_id = None

    the_real_message = message.reply_to_message or message
    try:
        await message.reply_text(
            f"<code>{the_real_message}</code>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❌ Close",
                            callback_data=f"close#{message.from_user.id}",
                        )
                    ]
                ]
            ),
        )
    except Exception as e:
        with open("json.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(the_real_message))
        await message.reply_document(
            document="json.text",
            caption=f"<code>{str(e)}</code>",
            disable_notification=True,
            reply_to_message_id=reply_to_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❌ Close",
                            callback_data=f"close#{message.from_user.id}",
                        )
                    ]
                ]
            ),
        )
        os.remove("json.text")


# Size Checker for Limit
def humanbytes(size: int):
    """Convert Bytes To Bytes So That Human Can Read It"""
    if not isinstance(command, int):
        try:
            size = size
        except ValueError:
            size = None
    if not size:
        return "0 B"
    size = int(size)
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {
        0: "",
        1: "K",
        2: "M",
        3: "G",
        4: "T",
        5: "P",
        6: "E",
        7: "Z",
        8: "Y",
    }
    while size > power:
        size /= power
        raised_to_pow += 1
    try:
        real_size = f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}B"
    except KeyError:
        real_size = "Can't Define Real Size !"
    return real_size


# Pattern if extension supported, PR if want to add more
pattern = compiles(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$|x-subrip$")


@vro.on_message(filters.command(["paste"], CUSTOM_CMD))
async def create(_, message):
    reply = message.reply_to_message
    target = str(message.command[0]).split("@", maxsplit=1)[0]
    if not reply and len(message.command) < 2:
        return await message.reply_text(f"**Reply To A Message With /{target} or with command**")

    msg = await message.reply_text("`Pasting to Rentry...`")
    data = ""
    limit = 1024 * 1024
    if reply and reply.document:
        if reply.document.file_size > limit:
            return await msg.edit(f"**You can only paste files smaller than {humanbytes(limit)}.**")
        if not pattern.search(reply.document.mime_type):
            return await msg.edit("**Only text files can be pasted.**")
        file = await reply.download()
        try:
            with open(file, "r") as text:
                data = text.read()
            remove(file)
        except UnicodeDecodeError:
            try:
                remove(file)
            except:
                pass
            return await msg.edit("`File Not Supported !`")
    elif reply and (reply.text or reply.caption):
        data = reply.text.markdown or reply.caption.markdown
    elif not reply and len(message.command) >= 2:
        data = message.text.split(None, 1)[1]

    if message.from_user:
        if message.from_user.username:
            uname = f"@{message.from_user.username}"
        else:
            uname = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    else:
        uname = message.sender_chat.title

    try:
        url = await rentry(data)
    except Exception as e:
        await msg.edit(f"`{e}`")
        return

    if not url:
        return await msg.edit("Text Too Short Or File Problems")
    button = [
        [InlineKeyboardButton("Open Link", url=url)],
        [InlineKeyboardButton("Share Link", url=f"https://telegram.me/share/url?url={url}")],
    ]

    pasted = f"**Successfully pasted your data to Rentry<a href='{url}'>.</a>\n\nPaste by {uname}**"
    await msg.edit(pasted, reply_markup=InlineKeyboardMarkup(button))


@vro.on_message(filters.command(["tpaste"], CUSTOM_CMD))
async def create(_, message):
    reply = message.reply_to_message
    target = str(message.command[0]).split("@", maxsplit=1)[0]
    if not reply and len(message.command) < 2:
        return await message.reply_text(f"**Reply To A Message With /{target} or with command**")

    msg = await message.reply_text("`Pasting to TempPaste...`")
    data = ""
    limit = 1024 * 1024
    if reply and reply.document:
        if reply.document.file_size > limit:
            return await msg.edit(f"**You can only paste files smaller than {humanbytes(limit)}.**")
        if not pattern.search(reply.document.mime_type):
            return await msg.edit("**Only text files can be pasted.**")
        file = await reply.download()
        try:
            with open(file, "r") as text:
                data = text.read()
            remove(file)
        except UnicodeDecodeError:
            try:
                remove(file)
            except:
                pass
            return await msg.edit("`File Not Supported !`")
    elif reply and (reply.text or reply.caption):
        data = reply.text.html or reply.caption.html
    elif not reply and len(message.command) >= 2:
        data = message.text.split(None, 1)[1]

    if message.from_user:
        if message.from_user.username:
            uname = f"@{message.from_user.username}"
        else:
            uname = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    else:
        uname = message.sender_chat.title

    try:
        req = await http.post(
            "https://tempaste.com/api/v1/create-paste/",
            data={
                "api_key": "xnwuzXubxk3kCUz9Q2pjMVR8xeTO4t",
                "title": "MissKaty Paste",
                "paste_content": data,
                "visibility": "public",
                "expiry_date_type": "months",
                "expiry_date": 12,
            },
        )
        url = f"https://tempaste.com/{json_loads(req.text)['url']}"
    except Exception as e:
        await msg.edit(f"`{e}`")
        return

    if not url:
        return await msg.edit("Text Too Short Or File Problems")
    button = [
        [InlineKeyboardButton("Open Link", url=url)],
        [InlineKeyboardButton("Share Link", url=f"https://telegram.me/share/url?url={url}")],
    ]

    pasted = f"**Successfully pasted your data to Tempaste<a href='{url}'>.</a>\n\nPaste by {uname}**"
    await msg.edit(pasted, reply_markup=InlineKeyboardMarkup(button))
