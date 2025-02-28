import discord
from discord.ext import commands, tasks
from datetime import datetime
import asyncio
import aiomysql

# Initialize bot
intents = discord.Intents.default()
intents.members = True  # Ensure member-related events work
bot = commands.Bot(command_prefix="$", intents=intents)

class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = None  # Ensure self.pool is initialized
        self.check_birthdays.start()  # Start the loop when the bot is initialized

    async def connect_db(self):
        """Establish a connection pool to the database."""
        if self.pool is None:  # Avoid re-initialization
            self.pool = await aiomysql.create_pool(
                host='uk02-sql.pebblehost.com',
                port=3306,
                user='customer_829856_VerificationSystemCCAC',
                password='eERjntoq!f@FEx10=X!pOmcr',
                db='customer_829856_VerificationSystemCCAC',
                autocommit=True
            )

            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("""
                        CREATE TABLE IF NOT EXISTS birthdays (
                            user_id BIGINT PRIMARY KEY,
                            birthday VARCHAR(5) NOT NULL
                        )
                    """)

    @commands.command()
    async def set_birthday(self, ctx, day: int, month: int):
        """Stores the birthday in the database."""
        if self.pool is None:
            await ctx.send("Database not connected. Please try again later.")
            return

        try:
            datetime(year=2024, month=month, day=day)  # Validate date
            birthday = f"{day:02d}-{month:02d}"

            async with self.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("""
                        INSERT INTO birthdays (user_id, birthday) 
                        VALUES (%s, %s) 
                        ON DUPLICATE KEY UPDATE birthday = VALUES(birthday)
                    """, (ctx.author.id, birthday))

            await ctx.send(f"Birthday set for {ctx.author.mention} on {birthday}!")
        except ValueError:
            await ctx.send("Invalid day or month. Please ensure the date is correct.")

    @tasks.loop(hours=24)
    async def check_birthdays(self):
        """Checks and announces birthdays."""
        if self.pool is None:
            print("Database not connected, skipping birthday check.")
            return

        today = datetime.now().strftime("%d-%m")

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT user_id FROM birthdays WHERE birthday = %s", (today,))
                birthdays = await cur.fetchall()

        for user_id, in birthdays:
            for guild in self.bot.guilds:
                user = guild.get_member(user_id)
                if user:
                    channel = discord.utils.get(guild.text_channels, name="general")
                    if channel:
                        await channel.send(f"HAPPY BIRTHDAYYY <3 {user.mention} 🎉🎂")
                    await asyncio.sleep(1)  

    @commands.command()
    async def list_birthdays(self, ctx):
        """Lists all stored birthdays."""
        if self.pool is None:
            await ctx.send("Database not connected. Please try again later.")
            return

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT user_id, birthday FROM birthdays")
                birthdays = await cur.fetchall()

        if birthdays:
            birthdays_list = "\n".join([f"<@{user_id}>: {date}" for user_id, date in birthdays])
            await ctx.send(f"Current birthdays:\n{birthdays_list}")
        else:
            await ctx.send("No birthdays have been set yet!")

async def setup(bot):
    birthday_cog = Birthday(bot)
    await birthday_cog.connect_db()  # Ensure database connection before adding the cog
    bot.add_cog(birthday_cog)
