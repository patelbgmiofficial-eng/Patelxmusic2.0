from pyrogram import filters
from pyrogram.types import Message, ChatPrivileges
from anony import app

# -------------------- PROMOTE -------------------- #
@app.on_message(filters.command("promote") & filters.reply)
async def promote(_, message: Message):
    user = message.reply_to_message.from_user
    try:
        await app.promote_chat_member(
            message.chat.id,
            user.id,
            ChatPrivileges(
                can_manage_chat=True,
                can_delete_messages=True,
                can_manage_video_chats=True,
                can_restrict_members=True,
                can_invite_users=True,
                can_pin_messages=True,
            )
        )
        await message.reply_text("✅ Admin ban gaya")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# -------------------- DEMOTE -------------------- #
@app.on_message(filters.command("demote") & filters.reply)
async def demote(_, message: Message):
    user = message.reply_to_message.from_user
    try:
        await app.promote_chat_member(
            message.chat.id,
            user.id,
            ChatPrivileges(
                can_manage_chat=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_invite_users=False,
                can_pin_messages=False,
            )
        )
        await message.reply_text("🚫 Demoted")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# -------------------- BAN -------------------- #
@app.on_message(filters.command("ban") & filters.reply)
async def ban(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Reply to user")

    user = message.reply_to_message.from_user

    try:
        member = await app.get_chat_member(message.chat.id, user.id)

        if member.status in ["administrator", "creator"]:
            return await message.reply_text("❌ Admin ko ban nahi kar sakta")

        await app.ban_chat_member(message.chat.id, user.id)

        await message.reply_text(f"⛔ {user.mention} Banned")

    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

# -------------------- UNBAN -------------------- #
@app.on_message(filters.command("unban") & filters.reply)
async def unban(_, message: Message):
    user = message.reply_to_message.from_user
    try:
        await app.unban_chat_member(message.chat.id, user.id)
        await message.reply_text("✅ Unbanned")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
