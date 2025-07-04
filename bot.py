import discord
from discord.ext import commands
import yt_dlp
import os
import sys

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.voice_states = True  # Needed for joining channels

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

@bot.event
async def on_ready():
    activity = discord.Game(name="Type !help for commands")
    print(f"Logged in as {bot.user}")

last_play_request = {}

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="Here's what I can do:",
        color=discord.Color.blue()
    )
    embed.add_field(name="!play <YouTube URL>", value="Get a prompt to play a YouTube video in your voice channel.", inline=False)
    embed.add_field(name="!stop", value="Stop playback, but stay in the voice channel.", inline=False)
    embed.add_field(name="!leave", value="Disconnect from the voice channel.", inline=False)
    embed.add_field(name="!help", value="Show this help message.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def play(ctx, url: str):
    if not ("youtube.com" in url or "youtu.be" in url):
        await ctx.send("Please provide a valid YouTube URL.")
        return

    msg = await ctx.send(f"{ctx.author.mention}, press ▶️ to play this video in your voice channel.")
    await msg.add_reaction("▶️")

    global last_play_request
    last_play_request = {
        "message_id": msg.id,
        "user_id": ctx.author.id,
        "url": url,
        "guild_id": ctx.guild.id
    }

@bot.command()
async def stop(ctx):
    """Stop playing audio, but stay connected to the voice channel."""
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await ctx.send("Playback stopped.")
    else:
        await ctx.send("Nothing is playing right now.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel.")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    global last_play_request
    play_req = last_play_request

    if (
        play_req
        and reaction.message.id == play_req.get("message_id")
        and user.id == play_req.get("user_id")
        and reaction.message.guild.id == play_req.get("guild_id")
        and str(reaction.emoji) == "▶️"
    ):
        voice = user.voice
        if not voice or not voice.channel:
            await reaction.message.channel.send(f"{user.mention}, you must be in a voice channel to play music!")
            return

        vc = reaction.message.guild.voice_client
        if not vc:
            vc = await voice.channel.connect()
        elif vc.channel != voice.channel:
            await vc.move_to(voice.channel)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'noplaylist': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(play_req["url"], download=False)
                if 'entries' in info:
                    info = info['entries'][0]
                audio_url = info['url']

            if vc.is_playing():
                vc.stop()

            source = discord.FFmpegPCMAudio(audio_url)
            vc.play(source)
            await reaction.message.channel.send(f"Now playing: {play_req['url']} in {voice.channel.mention}")

        except Exception as e:
            await reaction.message.channel.send(f"Failed to play: `{e}`")

if __name__ == "__main__":
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("Error: Please set the DISCORD_BOT_TOKEN environment variable!")
        sys.exit(1)
    bot.run(token)

