import discord
import json
import logging
from discord.ext import commands
from discord import app_commands
from datetime import datetime

from config.settings import TOKEN
import asyncio

# Set up logging
logging.basicConfig(level=logging.DEBUG)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents = intents)

@bot.event
async def on_ready():
  print(f'Logged on as {bot.user}!')
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)

async def load():
  # Load cogs
  for cog in ['test', 'results']:
    await bot.load_extension(f'cogs.{cog}')

async def main():
    try:
      async with bot:
        await load()
        await bot.start(TOKEN, log_handler=handler, log_level=logging.DEBUG)
    except asyncio.CancelledError:
        print("Main coroutine was cancelled.")

asyncio.run(main())