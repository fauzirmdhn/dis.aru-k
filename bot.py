import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import yt_dlp
import asyncio

load_dotenv()

async def search_ytdlp_async(query, ydl_opts):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: _extract(query, ydl_opts))

def _extract(query, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            return ydl.extract_info(query, download=False)
        except Exception as e:
            print(f"Error extracting info: {e}")
            return None

'''
Events structure :
async def EVENT(ARGS):

the EVENT is the name of the event you want to listen to
ARGS is the arguments that the event will pass to the function
self is needed in ARGS
'''
class Client(commands.Bot):
    async def on_ready(self):
        print(f'{self.user} successfully logged in')

        try:
            slashsync = await self.tree.sync()
            print(f"{len(slashsync)} synchronied")

        except Exception as e:
            print(f"error synchronizing: {e}")

    async def on_message(self, message):
        if message.author == self.user:
            return

Intents = discord.Intents.default()
Intents.message_content = True
Intents.guilds = True
Intents.members = True

client = Client(command_prefix='|', intents=Intents)

# SLASH COMMANDS
@client.tree.command(name="test", description="nodesc")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("iya iya, ga usah panggil aku, berisik tau.")

@client.tree.command(name="testargs", description="nodesc")
async def testargs(interaction: discord.Interaction, arg1: str):
    await interaction.response.send_message(f"kamu ngomong \"{arg1}\" ya?")

@client.tree.command(name="play", description="Adds a song to the queue and plays it")
@app_commands.describe(query="The name of the song to play")
async def play(interaction: discord.Interaction, st_query: str):
    await interaction.response.defer()

    voice_channel = interaction.user.voice.channel
    if not voice_channel:
        await interaction.followup.send("You need to be in a voice channel to use this command.")
        return
    
    voice_client = interaction.guild.voice_client
    if voice_client is None:
        voice_client = await voice_channel.connect()
    elif voice_channel != voice_client.channel:
        await voice_channel.move_to(voice_channel)

    ydl_opts = {
        "format": "bestaudio[abr<=96]/bestaudio",
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
    }

    query = "ytsearch1: " + st_query
    result = await search_ytdlp_async(query, ydl_opts)
    tracks = result.get("entries", [])

    if not tracks:
        await interaction.followup.send("No results found.")
        return
    
    first_track = tracks[0]
    audio_url = first_track.get["url"]
    title = first_track.get("title", "Untitled")

    ffmpeg_opts = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn -c:a libopus -b:a 96k",
    }

    source = discord.FFmpegOpusAudio(audio_url, **ffmpeg_opts, executable="bin\\ffmpeg\\ffmpeg.exe")
    voice_client.play(source)


client.run(os.getenv("TOKEN"))