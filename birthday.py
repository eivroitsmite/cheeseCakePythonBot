import discord
from discord.ext import tasks
from datetime import datetime
import asyncio

class Birthday:
    
    def __init__(self, bot):
        self.bot = bot
       
        self.user_birthdays = {}
        
    async def start_checking_birthdays(self):
        
        self.check_birthdays.start()

    async def set_birthday(self, ctx, day: int, month: int):
      
        try:
           
            datetime(year=2024, month=month, day=day)
            birthday = f"{day:02d}-{month:02d}"
            
            self.user_birthdays[ctx.author.id] = (birthday, ctx.guild.id)
            await ctx.send(f"Birthday set for {ctx.author.mention} on {birthday}!")
        except ValueError:
            await ctx.send("Invalid day or month. Please ensure the date is correct.")

    @tasks.loop(hours=24)
    async def check_birthdays(self):
        today = datetime.now().strftime("%d-%m")  
        for user_id, (birthday, guild_id) in self.user_birthdays.items():
            if birthday == today:
                guild = self.bot.get_guild(guild_id) 
                if guild:  
                    user = guild.get_member(user_id) 
                    if user:
                       
                        channel = discord.utils.get(guild.text_channels, name="general")
                        if channel:
                            await channel.send(f"HAPPY BIRTHDAYYY <3 {user.mention} 🎉🎂")
                        await asyncio.sleep(1)  

    async def list_birthdays(self, ctx):
     
        if self.user_birthdays:
            birthdays_list = "\n".join([f"<@{user_id}>: {date}" for user_id, (date, _) in self.user_birthdays.items()])
            await ctx.send(f"Current birthdays:\n{birthdays_list}")
        else:
            await ctx.send("No birthdays have been set yet!")
