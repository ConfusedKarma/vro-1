from bot import vro, OWNER_ID
from bot.helper.mirror_utils.download_utils.direct_link_generator import *
from pyrogram import filters
import regex as re

CUSTOM_CMD = ["/", "!"]

@vro.on_message(filters.command("byp", CUSTOM_CMD) & filters.regex(r"https?://[^\s]+") & filters.user(OWNER_ID))
async def byp(bot, update):
    url = update.matches[0].group(0)
    bsdk = sendcm(url)
    message = await update.reply_text(
        text=bsdk, disable_web_page_preview=True, quote=True
    )
