from re import L
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio
from datetime import datetime, timedelta
import sys, traceback

from responsehandler import ResponseHandler
from responsehandler import ALLOWED_CHANNELS
from booster import Giveaway

# Load environment variables
load_dotenv()

# Initialize helper classes
resH = ResponseHandler()
gift = Giveaway()

# Define bot intents and roles
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

ASSISTANT_ROLE_ID = 1243929202785386527
MODS_ROLE_ID = 1243559774847766619
ADMINS_ROLE_ID = 1243929060145631262
CO_OWNERS_ROLE_ID = 1243930541234065489
OWNERS_ROLE_ID = 1240455108047671406

# Define channels and interval
BOOST_CHANNEL_ID = 1244336805462016070
GENERAL_CHANNEL_ID = 123456789012345678  # Replace with the actual channel ID
INTRO_CHANNEL_ID = 123456789012345679    # Replace with the actual channel ID
ROLE_CHECK_INTERVAL = 60  # Interval to check roles in seconds

# Initialize bot
bot = commands.Bot(command_prefix='$', intents=intents)
warnings = {}
user_joined_times = {}



# @bot.command()
# async def load(ctx):
#     await bot.load_extension("cogs.mod")




# Load Discord token from environment variable
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if DISCORD_TOKEN is None:
    raise ValueError('Bot token not found. Please ensure the token variable is set correctly.')

@bot.event
async def on_ready():
    print(f'Yo, It\'s me, {bot.user}')

    for filename in os.listdir("./cogs"):
        if(filename.endswith('.py')): 
            print("Cog : " + filename[:-3] + " has been loaded")
            await bot.load_extension(f"cogs.{filename[:-3]}")
    
    # check_roles.start()  # Start role check task on bot startup

# @bot.event
# async def on_member_join(member):
#     """Handles a new member joining the server."""
#     general_channel = bot.get_channel(GENERAL_CHANNEL_ID)
#     intro_channel = bot.get_channel(INTRO_CHANNEL_ID)

#     # Send a welcome message and restrict initial channel permissions
#     if general_channel and intro_channel:
#         await general_channel.send(f"Welcome {member.mention}! Please visit {intro_channel.mention} and get a role within 48 hours to avoid being kicked.")
    
#     # Record the join time
#     user_joined_times[member.id] = datetime.now()

#     # Restrict the member’s view to only general and intro channels
#     for channel in member.guild.channels:
#         if channel.id not in [GENERAL_CHANNEL_ID, INTRO_CHANNEL_ID]:
#             await channel.set_permissions(member, view_channel=False)

# @tasks.loop(seconds=ROLE_CHECK_INTERVAL)
# async def check_roles():
#     """Periodically checks if users have obtained a role and kicks them if they haven't after 48 hours."""
#     current_time = datetime.now()
    
#     for member_id, join_time in list(user_joined_times.items()):
#         guild = bot.get_guild(GENERAL_CHANNEL_ID)  # Replace with the correct server ID
#         member = guild.get_member(member_id) if guild else None

#         # Only proceed if the member is still in the server and hasn't obtained any role beyond @everyone
#         if member and len(member.roles) <= 1:
#             if (current_time - join_time) > timedelta(hours=48):
#                 try:
#                     await member.kick(reason="Did not acquire a role within 48 hours.")
#                     await bot.get_channel(GENERAL_CHANNEL_ID).send(f"{member.name} was kicked for not getting a role within 48 hours.")
#                     del user_joined_times[member_id]  # Remove from tracking
#                 except discord.Forbidden:
#                     print(f"Could not kick {member.name}. Insufficient permissions.")
#                 except discord.HTTPException as e:
#                     print(f"Failed to kick {member.name} due to HTTP error: {e}")

# @bot.event
# async def on_member_remove(member):
#     """Clean up the tracking if a member leaves before getting a role."""
#     if member.id in user_joined_times:
#         del user_joined_times[member.id]

@bot.event
async def on_message(message):
    # Ignore bot messages and check allowed channels
    if message.author.bot or message.channel.id not in ALLOWED_CHANNELS:
        return

    # Use instance method for getting a response
    response = resH.get_response(message.content)
    if response:
        await message.channel.send(response)

    await bot.process_commands(message)

    

# Run the bot with your token and handle login errors
try:
    bot.run(DISCORD_TOKEN)
except discord.errors.LoginFailure as e:
    print(f"Failed to log in: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
