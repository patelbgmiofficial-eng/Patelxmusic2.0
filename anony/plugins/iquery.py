from pyrogram import filters
from anony import app

@app.on_inline_query()
async def inline_query(client, inline_query):
    await inline_query.answer(
        results=[],
        cache_time=1
    )
