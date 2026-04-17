import requests
import random
import string

from anony import app
from pyrogram import filters

# SAFE STORAGE
TEMPMAIL_DB = {}

def rand_pass():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


@app.on_message(filters.command("newmail"))
async def new_mail(client, message):
    uid = message.from_user.id

    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    dom = requests.get("https://api.mail.tm/domains").json()["hydra:member"][0]["domain"]

    email = f"{username}@{dom}"
    password = rand_pass()

    requests.post("https://api.mail.tm/accounts", json={
        "address": email,
        "password": password
    })

    token = requests.post("https://api.mail.tm/token", json={
        "address": email,
        "password": password
    }).json().get("token")

    if not token:
        return await message.reply("❌ Failed to create mail")

    TEMPMAIL_DB[uid] = {"email": email, "token": token}

    await message.reply(f"📧 Temp Mail Created:\n\n{email}")


@app.on_message(filters.command("inbox"))
async def inbox(client, message):
    uid = message.from_user.id

    if uid not in TEMPMAIL_DB:
        return await message.reply("❌ First use /newmail")

    token = TEMPMAIL_DB[uid]["token"]
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get("https://api.mail.tm/messages", headers=headers).json()
    msgs = r.get("hydra:member", [])

    if not msgs:
        return await message.reply("📭 Inbox empty")

    text = "📩 Latest Emails:\n\n"
    for i, m in enumerate(msgs[:5], 1):
        text += f"{i}. {m.get('subject','No Subject')}\n"

    await message.reply(text)
