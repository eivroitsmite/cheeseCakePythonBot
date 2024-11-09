import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)


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
        description=f"Prize: **{prize}**\nReact with 🎉 to enter!\nTime Remaining: {amount} {unit}\nParticipants: **0**",
        color=discord.Color.from_rgb(255, 105, 180)  # Pink color
    )
    embed.set_footer(text="Good luck to everyone!")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
    embed.set_image(url="https://media.discordapp.net/attachments/1243937626902364170/1244379120012623933/rawr4-removebg-preview.png?ex=671ca11d&is=671b4f9d&hm=6b6192219666ac4cebf22ac9492fd59336a8da5f9c46e65155b06426e70f03d9&=&format=webp&quality=lossless&width=471&height=465")

    giveaway_message = await ctx.send(embed=embed)
    await giveaway_message.add_reaction("🎉")

    participants = set()

    def check_add(reaction, user):
        return reaction.message.id == giveaway_message.id and str(reaction.emoji) == "🎉" and not user.bot

    def check_remove(reaction, user):
        return reaction.message.id == giveaway_message.id and str(reaction.emoji) == "🎉" and not user.bot

    async def track_reactions():
        nonlocal embed
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=1.0, check=check_add)
                if user not in participants:
                    participants.add(user)
                    embed.description = f"Prize: **{prize}**\nReact with 🎉 to enter!\nTime Remaining: {amount} {unit}\nParticipants: **{len(participants)}**"
                    await giveaway_message.edit(embed=embed)
            except asyncio.TimeoutError:
                pass

            try:
                reaction, user = await bot.wait_for("reaction_remove", timeout=1.0, check=check_remove)
                if user in participants:
                    participants.remove(user)
                    embed.description = f"Prize: **{prize}**\nReact with 🎉 to enter!\nTime Remaining: {amount} {unit}\nParticipants: **{len(participants)}**"
                    await giveaway_message.edit(embed=embed)
            except asyncio.TimeoutError:
                pass

    asyncio.create_task(track_reactions())
    await asyncio.sleep(duration)

    await giveaway_message.edit(embed=discord.Embed(
        title="🎉 **GIVEAWAY ENDED** 🎉",
        description=f"The giveaway for **{prize}** has ended! Choosing a winner...",
        color=discord.Color.pink()
    ))

    if participants:
        winner = random.choice(list(participants))
        winner_announcement = discord.Embed(
            title="🎉 **We have a winner!** 🎉",
            description=f"Congratulations {winner.mention}! You won **{prize}**!",
            color=discord.Color.pink()
        )
        winner_announcement.set_footer(text=f"Total Participants: {len(participants)}")
        await ctx.send(embed=winner_announcement)
    else:
        no_winner_announcement = discord.Embed(
            title="😢 **No Participants** 😢",
            description="Unfortunately, no one entered the giveaway.",
            color=discord.Color.pink()
        )
        await ctx.send(embed=no_winner_announcement)

@giveaway.error
async def giveaway_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to start a giveaway.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Usage: $giveaway <amount> <unit: seconds/minutes/hours> <prize>")