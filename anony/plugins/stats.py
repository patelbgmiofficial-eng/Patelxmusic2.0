from pyrogram import filters
from anony import app, db

@app.on_message(filters.command("stats"))
async def stats(client, message):
    m = message

    user = m.from_user.first_name if m.from_user else "User"

    _utext = m.lang["stats_user"].format(user=user) if hasattr(m, "lang") else f"Stats of {user}"

    await message.reply(_utext)
