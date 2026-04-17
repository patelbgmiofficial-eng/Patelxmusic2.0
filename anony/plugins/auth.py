from pyrogram import filters
from anony import app, db

@app.on_message(filters.command("auth"))
async def auth(_, message):
    m = message

    try:
        admins = await db.get_admins(m.chat.id, reload=True)
    except Exception:
        admins = []

    await message.reply(f"👮 Admin count: {len(admins)}")
