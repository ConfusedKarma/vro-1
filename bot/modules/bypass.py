from bot import app, SUDO_USERS
from bot.helper.mirror_utils.download_utils.direct_link_generator import *

import regex as re

CUSTOM_CMD = /

@app.on_message(filters.command("byp", CUSTOM_CMD) & filters.regex(r"https?://[^\s]+") & filters.user(SUDO_USERS))
async def byp(bot, update):
    url = update.matches[0].group(0)
    bsdk = shareus(url)
    message = await update.reply_text(
        text=bsdk, disable_web_page_preview=True, quote=True
    )
