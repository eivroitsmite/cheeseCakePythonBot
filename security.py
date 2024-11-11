import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import random
import string

REQUIRED_ROLE_ID = 1243576135481294859  
UNVERIFIED_ROLE_ID = 1305172270486126663 
WELCOME_CHANNEL_ID = 1305164254797893703  
NOTICE_CHANNEL_ID = 1305164254797893703 
NOTICE_MESSAGE = "You must get the 'Verified' role within 48 hours by sending the password I just DMed you in the notice channel."


from dbconn import (
    add_user,
    get_user_by_id,
    get_password_by_user_id,
    get_join_time_by_user_id,
    check_user_exists,
    delete_user_by_id
)

user_join_time = {}
user_passwords = {}  

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_roles.start() 

    def generate_password(self, length=8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        password = self.generate_password()
        # user_passwords[member.id] = password
        unverified_role = discord.utils.get(member.guild.roles, id=UNVERIFIED_ROLE_ID)
        
        if unverified_role:
            await member.add_roles(unverified_role, reason="New member - assigned Unverified role")

        add_user(member.id, datetime.now(), password)

        # user_join_time[member.id] = datetime.now()

        try:
            await member.send(
                f"Welcome to the server, {member.name}! Your verification password is: **{password}**.\n"
                f"Please send this password in the notice channel to get verified within 48 hours."
            )
        except discord.Forbidden:
            print(f"Could not send DM to {member.name}. They may have DMs disabled.")

        welcome_channel = self.bot.get_channel(WELCOME_CHANNEL_ID)
        if welcome_channel:
            await welcome_channel.send(
                f"Welcome {member.mention}! {NOTICE_MESSAGE}"
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.channel.id == NOTICE_CHANNEL_ID:
            member_id = message.author.id

            if check_user_exists(member_id) and message.content == get_password_by_user_id(member_id):
             
                verified_role = discord.utils.get(message.guild.roles, id=REQUIRED_ROLE_ID)
                unverified_role = discord.utils.get(message.guild.roles, id=UNVERIFIED_ROLE_ID)

                if verified_role:
                    await message.author.add_roles(verified_role, reason="Correct verification password provided.")
                if unverified_role:
                    await message.author.remove_roles(unverified_role, reason="Member verified - removed Unverified role")

                await message.channel.send(f"{message.author.mention} has been verified successfully!")
                
                delete_user_by_id(member_id)

    @tasks.loop(minutes=60)
    async def check_roles(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                if check_user_exists(member.id):
                    join_time = get_join_time_by_user_id(member.id)
                    if isinstance(join_time, str):
                        join_time = datetime.strptime(join_time, '%Y-%m-%d %H:%M:%S')
                        time_since_join = datetime.now() - join_time

                    if time_since_join >= timedelta(hours=48):
                        required_role = discord.utils.get(guild.roles, id=REQUIRED_ROLE_ID)
                        if required_role not in member.roles:
                            try:
                                await member.kick(reason="Failed to get required role within 48 hours.")
                                delete_user_by_id(member.id)
                            except discord.Forbidden:
                                print(f"Cannot kick {member.name}; insufficient permissions.")
                            except discord.HTTPException as e:
                                print(f"Error kicking {member.name}: {e}")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        delete_user_by_id(member.id)

    def cog_unload(self):
        self.check_roles.cancel()
