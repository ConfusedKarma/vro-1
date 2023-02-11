from bot import vro, OWNER_ID
from bot.helper.mirror_utils.download_utils.direct_link_generator import *
from pyrogram import filters
import regex as re
from bot.helper.ext_utils.bot_utils import authorized_chats
CUSTOM_CMD = ["/", "!"]

@vro.on_message(filters.command("byp", CUSTOM_CMD) & filters.regex(r"https?://[^\s]+"))
@authorized_chats
async def byp(bot, update):
    url = update.matches[0].group(0)
    bsdk = xpshort(url)
    message = await update.reply_text(
        text=bsdk, disable_web_page_preview=True, quote=True
    )

@vro.on_message(filters.command("t", CUSTOM_CMD) & filters.regex(r"https?://[^\s]+"))
@authorized_chats
async def byp(bot, update):
    url = update.matches[0].group(0)
    bsdk = terabox(url)
    message = await update.reply_text(
        text=bsdk, disable_web_page_preview=True, quote=True
    )

@vro.on_message(filters.command("rc", CUSTOM_CMD) & filters.regex(r"https?://[^\s]+"))
@authorized_chats
async def byp(bot, update):
    url = update.matches[0].group(0)
    bsdk = rock(url)
    message = await update.reply_text(
        text=bsdk, disable_web_page_preview=True, quote=True
    )
@vro.on_message(filters.command("gp", CUSTOM_CMD) & filters.regex(r"https?://[^\s]+"))
@authorized_chats
async def byp(bot, update):
    url = update.matches[0].group(0)
    bsdk = gplinks(url)
    message = await update.reply_text(
        text=bsdk, disable_web_page_preview=True, quote=True
    )
