from pyrogram import filters
from anony import app
import os
import sys

@app.on_message(filters.command("restart"))
async def restart(_, message):
    await message.reply_text("♻️ Restarting bot...")

    os.execv(sys.executable, ["python3", "-m", "anony"])
