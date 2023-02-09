from bot import vro, OWNER_ID

CUSTOM_CMD = ["/", "!"]


import os

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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


@vro.on_message(filters.incoming & filters.private)
async def frwd(message):
  try:
    USER_ID = message.from_user.mention
    await vro.forward_message(message.from_user.id, OWNER_ID)
  except:
    vro.send_message(OWNER_ID, f"{USER_ID} is spamming me! I am not able to forward his messages")
