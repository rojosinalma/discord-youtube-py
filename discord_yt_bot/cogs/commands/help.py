from discord.ext import commands
import discord


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
            title="Bot Commands",
            description="Here's what I can do:",
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="!play <YouTube URL>",
            value="Get a prompt to play a YouTube video in your voice channel.",
            inline=False,
        )
        embed.add_field(
            name="!stop",
            value="Stop playback, but stay in the voice channel.",
            inline=False,
        )
        embed.add_field(
            name="!leave", value="Disconnect from the voice channel.", inline=False
        )
        embed.add_field(name="!help", value="Show this help message.", inline=False)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
