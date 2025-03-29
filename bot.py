import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

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
            guild = discord.Object(id=1265992956209266800)
            slashsync = await self.tree.sync(guild=guild)
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

GUILD_ID = discord.Object(id=1265992956209266800)

# SLASH COMMANDS
@client.tree.command(name="test", description="nodesc", guild=GUILD_ID)
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("iya iya, ga usah panggil aku, berisik tau.")

@client.tree.command(name="testargs", description="nodesc", guild=GUILD_ID)
async def testargs(interaction: discord.Interaction, arg1: str):
    await interaction.response.send_message(f"kamu ngomong \"{arg1}\" ya?")

client.run(os.getenv("TOKEN"))