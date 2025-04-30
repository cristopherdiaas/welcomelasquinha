import discord
from discord.ext import commands
import dotenv
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = 1244309451507241012  # Substitua pelo ID do canal de boas-vindas


# Mapeamento de insígnias públicas
def get_user_badges(public_flags: discord.PublicUserFlags):
    badge_names = {
        "staff": "👨‍💼 Discord Staff",
        "partner": "🤝 Partner",
        "hypesquad_bravery": "🦁 Bravery",
        "hypesquad_balance": "⚖️ Balance",
        "hypesquad_brilliance": "🧠 Brilliance",
        "bug_hunter": "🐞 Bug Hunter",
        "verified_bot": "🤖 Verified Bot",
        "early_supporter": "🎟️ Early Supporter",
        "active_developer": "💻 Active Dev"
    }

    badges = []
    for badge, label in badge_names.items():
        if getattr(public_flags, badge, False):
            badges.append(label)
    return badges


# Função principal de boas-vindas com embed
async def send_welcome_embed(member: discord.Member, channel: discord.TextChannel):
    embed = discord.Embed(
        title="🎉 Boas-vindas!",
        description=f"Olá {member.mention}, bem-vindo(a) ao servidor **{member.guild.name}**!",
        color=discord.Color.purple()
    )

    embed.set_thumbnail(url=member.display_avatar.url)

    # Insígnias
    badges = get_user_badges(member.public_flags)
    embed.add_field(
        name="🏅 Insígnias",
        value=", ".join(badges) if badges else "Nenhuma",
        inline=False
    )

    # Cargos (excluindo @everyone)
    roles = [role.name for role in member.roles if role.name != "@everyone"]
    embed.add_field(
        name="🎭 Cargos",
        value=", ".join(roles[:3]) if roles else "Nenhum",
        inline=False
    )

    embed.set_footer(text=f"ID: {member.id}")
    await channel.send(embed=embed)


# Evento de entrada no servidor
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await send_welcome_embed(member, channel)


# Comando de teste manual
@bot.command()
async def testwelcome(ctx):
    await send_welcome_embed(ctx.author, ctx.channel)


# Inicie o bot
bot.run(TOKEN)