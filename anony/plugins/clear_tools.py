from pyrogram import filters
from anony import app


# ───────── CLEAR / DELETE (BOT SAFE) ─────────
@app.on_message(filters.command(["clear", "delete"]))
async def clear_messages(_, message):

    chat_id = message.chat.id

    try:
        # Telegram bot safe bulk delete (last 50 via message IDs workaround)
        if not message.reply_to_message:
            return await message.reply("❌ Reply to a message to start clearing")

        start_id = message.reply_to_message.id
        current_id = message.id

        deleted = 0

        for msg_id in range(start_id, current_id + 1):
            try:
                await app.delete_messages(chat_id, msg_id)
                deleted += 1
            except:
                pass

        await message.reply(f"🧹 Deleted {deleted} messages")
    except Exception as e:
        await message.reply(f"Error: {e}")
