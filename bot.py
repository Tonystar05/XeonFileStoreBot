#
# # ⚠️ Please don't change our credits 𝚃𝙷𝙰𝙽𝙺𝚂 𝚃𝙾 & 𝙳𝙴𝚅 👇🏻
# ©️ Copyright (C) 2025 by https://t.me/Xeonflix 
# All rights reserved.
# ====================(@XEONFLIX)========================#

from aiohttp import web
from plugins import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
import logging
from config import *
from database.database import db  # Updated import

name = """『X E O N F L I X _ B O T』"""

# Configure custom logging formatter to display only the message
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',  # Only the message, no timestamp or level
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = logging.getLogger(__name__)

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Load settings from database
        global PROTECT_CONTENT, HIDE_CAPTION, DISABLE_CHANNEL_BUTTON, BUTTON_NAME, BUTTON_LINK
        settings = await db.get_settings()
        PROTECT_CONTENT = settings.get('PROTECT_CONTENT', False)
        HIDE_CAPTION = settings.get('HIDE_CAPTION', False)
        DISABLE_CHANNEL_BUTTON = settings.get('DISABLE_CHANNEL_BUTTON', True)
        BUTTON_NAME = settings.get('BUTTON_NAME', None)
        BUTTON_LINK = settings.get('BUTTON_LINK', None)

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER.warning(e)
            self.LOGGER.warning(f"ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ᴅʙ ᴄʜᴀɴɴᴇʟ, ᴀɴᴅ ᴅᴏᴜʙʟᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ_ɪᴅ ᴠᴀʟᴜᴇ, ᴄᴜʀʀᴇɴᴛ ᴠᴀʟᴜᴇ {CHANNEL_ID}")
            self.LOGGER.info("\nʙᴏᴛ sᴛᴏᴘᴘᴇᴅ. ᴊᴏɪɴ https://t.me/Anime_Lord_Support ғᴏʀ sᴜᴘᴘᴏʀᴛ")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER.info(f"ʙᴏᴛ ɪs ᴀʟɪᴠᴇ..!\n\nᴄʀᴇᴀᴛᴇᴅ ʙʏ \n 『ᴀɴɪᴍᴇ-ʟᴏʀᴅ-ʙᴏᴛ』\nʙᴏᴛ ᴅᴇᴘʟᴏʏᴇᴅ ʙʏ @ᴡʜᴏ-ᴀᴍ-ɪ\nʙᴏᴛ ɪs ᴀʟɪᴠᴇ..! ᴍᴀᴅᴇ ʙʏ @ᴀɴɪᴍᴇ ʟᴏʀᴅ\nʙᴏᴛ ɪs ɴᴏᴡ ᴀʟɪᴠᴇ. ᴛʜᴀɴᴋs ᴛᴏ @ᴡʜᴏ-ᴀᴍ-ɪ\n▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄\n|------------------『X E O N F L I X  B O T』----------------------|\n▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀▄▀\n               ◈◈◈◈◈◈ ɪ_s_ᴀ_ʟ_ɪ_ᴠ_ᴇ ◈◈◈◈◈◈  \n                       ▼   ᴀᴄᴄᴇssɪɴɢ   ▼  \n                         ███████] 99%")
        self.username = usr_bot_me.username

        # sᴛᴀʀᴛ ᴡᴇʙ sᴇʀᴠᴇʀ
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()

        try:
            await self.send_message(OWNER_ID, text=f"<b><blockquote>ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ ʙʏ @XeOnFlIx</blockquote></b>")
        except Exception as e:
            self.LOGGER.warning(f"ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ sᴛᴀʀᴛᴜᴘ ᴍᴇssᴀɢᴇ ᴛᴏ OWNER_ID: {str(e)}")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER.info("ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ.")

    def run(self):
        """Run the bot."""
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER.info("ғᴜᴄᴋɪɴ ᴅᴏᴡɴ...")
        finally:
            loop.run_until_complete(self.stop())

#
# # ⚠️ Please don't change our credits 𝚃𝙷𝙰𝙽𝙺𝚂 𝚃𝙾 & 𝙳𝙴𝚅 👇🏻
# ©️ Copyright (C) 2025 by https://t.me/Xeonflix 
# All rights reserved.
# ====================(@XEONFLIX)========================#
