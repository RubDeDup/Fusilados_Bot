import discord
from discord.ext import commands, tasks
from datetime import datetime, time

TOKEN = 'DISCORD_TOKEN_HIER'
PLANNING_CHANNEL_ID = Kanaal van de planning berichten hier
SCOREBORD_CHANNEL_ID = Kanaal van het scorebord hier

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

maand_data = {}
huidige_maand_naam = datetime.now().strftime('%B')

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online!')
    maandelijkse_check.start()
    dagelijks_scorebord.start() # Start de dagelijkse taak om 20:00

# --- AUTOMATISCH SCOREBORD OM 20:00 ---
@tasks.loop(time=time(hour=20, minute=0))
async def dagelijks_scorebord():
    channel = bot.get_channel(SCOREBORD_CHANNEL_ID)
    if channel:
        await stuur_scorebord(channel)

# --- MAANDELIJKSE CHECK ---
@tasks.loop(hours=24)
async def maandelijkse_check():
    global huidige_maand_naam
    nieuwe_maand_naam = datetime.now().strftime('%B')
    if nieuwe_maand_naam != huidige_maand_naam:
        huidige_maand_naam = nieuwe_maand_naam

# --- REACTIE LOGICA (PUNTEN TELEN) ---
@bot.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != PLANNING_CHANNEL_ID or payload.user_id == bot.user.id:
        return
    if str(payload.emoji) == "🟢":
        if huidige_maand_naam not in maand_data:
            maand_data[huidige_maand_naam] = {}
        maand_data[huidige_maand_naam][payload.user_id] = maand_data[huidige_maand_naam].get(payload.user_id, 0) + 1

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.channel_id != PLANNING_CHANNEL_ID or payload.user_id == bot.user.id:
        return
    if str(payload.emoji) == "🟢":
        if huidige_maand_naam in maand_data and payload.user_id in maand_data[huidige_maand_naam]:
            maand_data[huidige_maand_naam][payload.user_id] = max(0, maand_data[huidige_maand_naam][payload.user_id] - 1)

# --- HULPFUNCTIE OM SCOREBORD TE MAKEN ---
async def stuur_scorebord(channel):
    if not maand_data or all(not scores for scores in maand_data.values()):
        await channel.send("📊 Het scorebord is voorlopig nog leeg.")
        return

    embed = discord.Embed(title="🏆 Dagelijks Aanwezigheden Scorebord", color=discord.Color.gold())
    
    for maand, scores in maand_data.items():
        if not scores: continue
        gesorteerd = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        beschrijving = ""
        for index, (user_id, punten) in enumerate(gesorteerd, start=1):
            user = channel.guild.get_member(user_id)
            naam = user.display_name if user else f"Speler ({user_id})"
            embleem = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else f"{index}."
            beschrijving += f"{embleem} **{naam}** — `{punten}`\n"
        embed.add_field(name=f"📅 {maand}", value=beschrijving, inline=False)
    
    await channel.send(embed=embed)

# --- COMMANDO VOOR HANDMATIG SCOREBORD ---
@bot.command()
async def scorebord(ctx):
    await stuur_scorebord(ctx.channel)

# --- ALTIJD ALS ALLERLAATSTE ---
bot.run(TOKEN)
