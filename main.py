import discord
import logging
from discord.ext import commands
from logging.handlers import RotatingFileHandler
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

handler = RotatingFileHandler(
    filename='logs/ICE5.log',
    encoding='utf-8',
    mode='a',
    maxBytes=32 * 1024 * 1024,
    backupCount=5
)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[handler, logging.StreamHandler()])


@bot.event
async def on_ready():
    logging.info(f'Bot logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.channel.name != "whitelist-requests":
        return

    if message.author == bot.user:
        return

    minecraft_username = message.content.split(" ")[0]
    minecraft_username_filtered = ''.join(i for i in minecraft_username if i.isalnum())

    if len(minecraft_username_filtered) > 0:
        rcon_command = f"~/scripts/rcon.sh whitelist add {minecraft_username_filtered}"
        logging.info(f"whitelist-requests command executed: {rcon_command}")
        os.system(rcon_command)
        await message.channel.send(f'Додано {minecraft_username_filtered}')


def get_token() -> str:
    try:
        with open('token.txt', 'r') as f:
            token = f.readline().strip()
        return token
    except FileNotFoundError as e:
        logging.critical('token must be specified in the %r file', e.filename)
        raise SystemExit(1)


TOKEN = get_token()
bot.run(TOKEN)
