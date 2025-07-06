import os
import sys
import discord
from discord.ext import commands


def create_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True
    intents.reactions = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
    return bot


async def load_cogs(bot: commands.Bot) -> None:
    await bot.load_extension("discord_yt_bot.cogs.commands.help")
    await bot.load_extension("discord_yt_bot.cogs.commands.music")
    await bot.load_extension("discord_yt_bot.cogs.events.ready")
    await bot.load_extension("discord_yt_bot.cogs.events.reactions")


def main() -> None:
    bot = create_bot()

    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("Error: Please set the DISCORD_BOT_TOKEN environment variable!")
        sys.exit(1)

    bot.loop.create_task(load_cogs(bot))
    bot.run(token)


if __name__ == "__main__":
    main()
