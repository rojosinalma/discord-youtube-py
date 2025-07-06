import discord
from discord.ext import commands
from discord_yt_bot.utils.youtube import extract_audio_url


class ReactionHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User) -> None:
        if user.bot:
            return

        music_cog = self.bot.get_cog("Music")
        if not music_cog or not hasattr(music_cog, "last_play_request"):
            return

        play_req = music_cog.last_play_request

        if (
            play_req
            and reaction.message.id == play_req.get("message_id")
            and user.id == play_req.get("user_id")
            and reaction.message.guild.id == play_req.get("guild_id")
            and str(reaction.emoji) == "\u25B6\uFE0F"
        ):
            voice = user.voice
            if not voice or not voice.channel:
                await reaction.message.channel.send(
                    f"{user.mention}, you must be in a voice channel to play music!"
                )
                return

            vc = reaction.message.guild.voice_client
            if not vc:
                vc = await voice.channel.connect()
            elif vc.channel != voice.channel:
                await vc.move_to(voice.channel)

            try:
                audio_url = extract_audio_url(play_req["url"])

                if vc.is_playing():
                    vc.stop()

                source = discord.FFmpegPCMAudio(audio_url)
                vc.play(source)
                await reaction.message.channel.send(
                    f"Now playing: {play_req['url']} in {voice.channel.mention}"
                )
            except Exception as e:
                await reaction.message.channel.send(f"Failed to play: `{e}`")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ReactionHandler(bot))
