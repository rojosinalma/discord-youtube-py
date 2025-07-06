from discord.ext import commands
import discord


class ReadyEvent(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        activity = discord.Game(name="Type !help for commands")
        if self.bot.user:
            print(f"Logged in as {self.bot.user}")
        await self.bot.change_presence(activity=activity)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReadyEvent(bot))
