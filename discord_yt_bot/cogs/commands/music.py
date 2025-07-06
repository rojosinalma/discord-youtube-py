import discord
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.last_play_request = {}

    @commands.command()
    async def play(self, ctx: commands.Context, url: str) -> None:
        if "youtube.com" not in url and "youtu.be" not in url:
            await ctx.send("Please provide a valid YouTube URL.")
            return

        msg = await ctx.send(
            f"{ctx.author.mention}, press \u25B6\uFE0F to play this video in your voice channel."
        )
        await msg.add_reaction("\u25B6\uFE0F")

        self.last_play_request = {
            "message_id": msg.id,
            "user_id": ctx.author.id,
            "url": url,
            "guild_id": ctx.guild.id,
        }

    @commands.command()
    async def stop(self, ctx: commands.Context) -> None:
        """Stop playing audio, but stay connected to the voice channel."""
        vc = ctx.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await ctx.send("Playback stopped.")
        else:
            await ctx.send("Nothing is playing right now.")

    @commands.command()
    async def leave(self, ctx: commands.Context) -> None:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Left the voice channel.")
        else:
            await ctx.send("I'm not in a voice channel.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))
