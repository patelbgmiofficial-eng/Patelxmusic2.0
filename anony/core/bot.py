import pyrogram
from anony import config, logger


class Bot(pyrogram.Client):
    def __init__(self):
        super().__init__(
            name="Anony",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=pyrogram.enums.ParseMode.HTML
        )

        self.owner = config.OWNER_ID
        self.logger = config.LOGGER_ID

        # FIXED (no filters.user() here)
        self.sudoers = [self.owner]
        self.bl_users = set()

    async def boot(self):
        await super().start()

        self.id = self.me.id
        self.name = self.me.first_name
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(self.logger, "Bot Started")
            get = await self.get_chat_member(self.logger, self.id)

        except Exception as ex:
            raise SystemExit(
                f"Bot failed to access log group: {self.logger}\nReason: {ex}"
            )

        if get.status != pyrogram.enums.ChatMemberStatus.ADMINISTRATOR:
            raise SystemExit("Make bot admin in logger group")

        logger.info(f"Bot started as @{self.username}")

    async def exit(self):
        await super().stop()
        logger.info("Bot stopped.")
