import discord
import random
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='$', description="Cheesecake", intents=intents)

class Giveaway:
    @staticmethod
    def convert_time(amount: int, unit: str):
        if unit == "seconds":
            return amount
        elif unit == "minutes":
            return amount * 60
        elif unit == "hours":
            return amount * 3600
        else:
            raise ValueError("Invalid time unit")

@bot.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx, amount: int, unit: str, *, prize: str):
    try:
        duration = Giveaway.convert_time(amount, unit)
    except ValueError:
        await ctx.send("Please use a valid time unit: `seconds`, `minutes`, or `hours`.")
        return

    embed = discord.Embed(
        title="🎉 **GIVEAWAY TIME!** 🎉",
        description=f"Prize: **{prize}**\nReact with 🎉 to enter!\nTime Remaining: {amount} {unit}",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Good luck to everyone!")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

    giveaway_message = await ctx.send(embed=embed)
    await giveaway_message.add_reaction("🎉")

    participants = set()  # Using a set to store participants and avoid duplicates

    def check(reaction, user):
        return reaction.message.id == giveaway_message.id and str(reaction.emoji) == "🎉" and not user.bot

    # Tracking users joining and leaving
    async def track_reactions():
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=5.0, check=check)
                if user not in participants:
                    participants.add(user)
                    await user.send(f"You have joined the giveaway for **{prize}**! Good luck!")
            except asyncio.TimeoutError:
                break

            try:
                reaction, user = await bot.wait_for("reaction_remove", timeout=5.0, check=check)
                if user in participants:
                    participants.remove(user)
                    await user.send(f"You have left the giveaway for **{prize}**.")
            except asyncio.TimeoutError:
                break

    asyncio.create_task(track_reactions())
    await asyncio.sleep(duration)

    # Update the message to show the giveaway has ended
    await giveaway_message.edit(embed=discord.Embed(
        title="🎉 **GIVEAWAY ENDED** 🎉",
        description=f"The giveaway for **{prize}** has ended! Choosing a winner...",
        color=discord.Color.dark_gray()
    ))

    # Determine the winner
    if participants:
        winner = random.choice(list(participants))
        winner_announcement = discord.Embed(
            title="🎉 **We have a winner!** 🎉",
            description=f"Congratulations {winner.mention}! You won **{prize}**!",
            color=discord.Color.green()
        )
        winner_announcement.set_footer(text=f"Total Participants: {len(participants)}")
        await ctx.send(embed=winner_announcement)
    else:
        no_winner_announcement = discord.Embed(
            title="😢 **No Participants** 😢",
            description="Unfortunately, no one entered the giveaway.",
            color=discord.Color.red()
        )
        await ctx.send(embed=no_winner_announcement)

@giveaway.error
async def giveaway_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to start a giveaway.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: $giveaway <amount> <unit: seconds/minutes/hours> <prize>")
