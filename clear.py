import discord
from discord.ext import commands

# Vul hier je Discord bot-token in (mag dezelfde zijn als je andere bots)
TOKEN = 'DISCORD_TOKEN_HIER'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Clear-bot is online en klaar voor gebruik!')

# --- COMMANDO: !clear ---
@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    if amount > 100:
        await ctx.send("❌ Je kunt maximaal 100 berichten tegelijk verwijderen.", delete_after=5)
        return

    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"🧹 {len(deleted) - 1} berichten succesvol verwijderd.", delete_after=4)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Jij hebt geen toestemming om berichten te wissen.", delete_after=5)
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Geef een geldig getal op (bijvoorbeeld `!clear 10`).", delete_after=5)

bot.run(TOKEN)
