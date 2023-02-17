from telegram.ext import CommandHandler

from bot import LOGGER, dispatcher, vro
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from bot.helper.ext_utils.bot_utils import new_thread, is_gdrive_link
from bot.helper.telegram_helper.message_utils import sendMessage, deleteMessage
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.filters import CustomFilters

from pyrogram import filters
import PyBypass as bypasser

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
async def bypass(_, msg):
    nam = None
    m = msg.text.split()
    
    if len(m)<2:
        await msg.reply_text("Format: /bypass <url> <name only if required>", parse_mode="markdown")
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
