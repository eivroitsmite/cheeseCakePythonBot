import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

from responsehandler import ResponseHandler
from responsehandler import ALLOWED_CHANNELS
from giveaway import Giveaway

load_dotenv()

resH = ResponseHandler()
gift = Giveaway()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

ASSISTANT_ROLE_ID = 1243929202785386527
MODS_ROLE_ID = 1243559774847766619
ADMINS_ROLE_ID = 1243929060145631262
CO_OWNERS_ROLE_ID = 1243930541234065489
OWNERS_ROLE_ID = 1240455108047671406

BOOST_CHANNEL_ID = 1244336805462016070
BUMP_CHANNEL_ID = 1247358259031969843 

bot = commands.Bot(command_prefix='$', intents=intents)

warnings = {}

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if DISCORD_TOKEN is None:
    raise ValueError('Bot token not found. Please ensure the token variable is set correctly.')

@bot.event
async def on_ready():
    print(f'Yo, It\'s me, {bot.user}')
    
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            print("Cog : " + filename[:-3] + " has been loaded")
            await bot.load_extension(f"cogs.{filename[:-3]}")
    
    bump_task.start()

@bot.event
async def on_message(message):
    if message.author.bot or message.channel.id not in ALLOWED_CHANNELS:
        return

    response = resH.get_response(message.content)
    if response:
        await message.channel.send(response)

    await bot.process_commands(message)

@tasks.loop(hours=2)
async def bump_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(BUMP_CHANNEL_ID)
    
    if isinstance(channel, discord.TextChannel): 
        await channel.send("/bump")
    else:
        print(f"Channel {BUMP_CHANNEL_ID} is not a TextChannel, cannot send messages.")


try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
    print(f"Failed to log in: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
