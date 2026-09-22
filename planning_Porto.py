import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timezone
import random  # <--- Dit zorgt voor de willekeurige getallen!

# Vul hier je eigen gegevens in
TOKEN = 'DISCORD_TOKEN_HIER'
CHANNEL_ID = ID_VAN_PLANNINGKANAAL_HIER

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online en klaar voor de planning!')
    dagelijks_bericht.start()

# --- 1. DE DAGELIJKSE TIMER ---
@tasks.loop(time=time(hour=9, minute=0, tzinfo=timezone.utc))
async def dagelijks_bericht():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Pakt elke dag een random getal tussen 69 en 999
        random_kanaal = random.randint(69, 999)
        
        embed = discord.Embed(
            title="📅 Planning voor Vandaag!",
            description=f"Wie is er aanwezig? Reageer met de emoji's hieronder!\n\n"
                        f"📻 **Porto-kanaal van de dag:** Kanaal {random_kanaal}\n\n"
                        f"🟢 = Aanwezig\n"
                        f"🔴 = Niet aanwezig",
            color=discord.Color.blue()
        )
        bericht = await channel.send(embed=embed)
        await bericht.add_reaction("🟢")
        await bericht.add_reaction("🔴")

# --- 2. HET TEST COMMANDO ---
@bot.command()
async def testplan(ctx):
    # Ook het testcommando krijgt een random kanaal om te zien of het werkt!
    random_kanaal = random.randint(69, 999)
    
    embed = discord.Embed(
        title="📅 Planning voor Vandaag!",
        description=f"Wie is er aanwezig? Reageer met de emoji's hieronder!\n\n"
                    f"📻 **Porto-kanaal van de dag:** Kanaal {random_kanaal}\n\n"
                    f"🟢 = Aanwezig\n"
                    f"🔴 = Niet aanwezig",
        color=discord.Color.blue()
    )
    bericht = await ctx.send(embed=embed)
    await bericht.add_reaction("🟢")
    await bericht.add_reaction("🔴")

# --- 3. ALTIJD ALS ALLERLAATSTE ---
bot.run(TOKEN)
