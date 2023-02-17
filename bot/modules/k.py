from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher, vro
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.ext_utils.bot_utils import new_thread, is_gdrive_link
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters

import requests
from pyrogram import filters
import PyBypass as bypasser

from bot.helper.ext_utils.bot_utils import authorized_chats

@new_thread
def permissionNode(update, context):
    args = update.message.text.split()
    reply_to = update.message.reply_to_message
    link = ''
    access = ''
    if len(args) > 1:
        link = args[1].strip()
        try:
            access = args[2].strip()
        except IndexError:
            pass
    if reply_to:
        link = reply_to.text.split(maxsplit=1)[0].strip()
        try:
            access = args[1].strip()
        except IndexError:
            pass
    if is_gdrive_link(link):
        msg = sendMessage(f"<b>Setting permission:</b> <code>{link}</code>", context.bot, update.message)
        LOGGER.info(f"Setting permission: {link}")
        gd = GoogleDriveHelper()
        result = gd.setPermission(link, access)
        deleteMessage(context.bot, msg)
        sendMessage(result, context.bot, update.message)
    else:
        sendMessage("<b>Send a Drive link along with command</b>", context.bot, update.message)

permission_handler = CommandHandler(BotCommands.PermissionCommand, permissionNode,
                                    filters=CustomFilters.owner_filter)
dispatcher.add_handler(permission_handler)

@vro.on_message(filters.command('bypass'))
@authorized_chats
async def bypass(_, msg):
    nam = None
    m = msg.text.split()
    
    if len(m)<2:
        await msg.reply_text("/bypass <url> <name only if required>")
        return
    if len(m)>2:
        nam = m[2]
        
    url = m[1]
    x = await msg.reply_text(f"Trying to Bypass __`{url}`__...")

    try:
        if nam!=None:
            bypassed = bypasser.bypass(url, name=nam)
        bypassed = bypasser.bypass(url)
    except Exception as e:
        await x.delete()
        await msg.reply_text(f"Couldn't bypass {url}\nError: {e}")
        return

    await x.delete()
    await msg.reply_text(f"**BYPASSED URL:** `{bypassed}`")

@vro.on_message(filters.command('gdtot'))
@authorized_chats
async def gdtotbypass(_, msg):
    m = msg.text.split()
    
    if len(m)<3:
        await msg.reply_text("Format: /gdtot <url> <gdtot crypt>")
        return
    
    url = m[1]
    crypt = m[2]
    
    x = await msg.reply_text(f"Trying to Bypass __`{url}`__...")
    
    try:
        bypassed = bypasser.bypass(url, gdtot_crypt=crypt)
    except Exception as e:
        await x.delete()
        await msg.reply_text(f"Couldn't bypass {url}\nError: {e}")
        return

    await x.delete()
    await msg.reply_text(f"**BYPASSED URL:** `{bypassed}`")
    return

SUPPORTED_FILE_TYPES = [".html", ".txt", ".log"]

def paste(text):
    url = "https://spaceb.in/api/v1/documents/"
    res = requests.post(url, data={"content": text, "extension": "txt"})
    if res.status_code>200:
        return f"https://spaceb.in/{res.json()['payload']['id']}"
    else:
        LOGGER.info("Getting low status code/\Func: paste")
        return
    

@vro.on_message(filters.command('paste'))
@authorized_chats
async def pastewo(_, msg):
    status_msg = await msg.reply_text("Processing...")
    reply = msg.reply_to_message
    
    if reply:
        if reply.text:
            text = msg.reply_to_message.text
        if reply.document and (reply.document.file_size<(10 * 1024**2)):
            # any(file_name.endswith(s) for s in SUPPORTED_FILE_TYPES)
            
            try:
                path = await reply.download()
                with open(path) as data:
                    text = data.read()
                    
            except Exception as e:
                LOGGER.info(e, "caused by FUNC: pasteowo")
                await msg.reply(f"Sorry some error excured\nERROR: {e}")
                return
            
    else:
        m = msg.text.split()
        if len(m)<2:
            await msg.reply_text("Format: /paste <reply_to_msg/text>")
        text = m[1]
    
    try:
        pasted = paste(text)
    except Exception as e:
        await msg.reply_text(f"Some error occurred, probably API down.\nERROR: {e}")
        LOGGER.info(e)
        return
        
    await msg.reply_text(f"Pasted to **Spacebin**: {pasted}")
    await status_msg.delete()
    return 
