import discord
import json
import logging
from discord.ext import commands
from discord import app_commands
from datetime import datetime

from config.settings import TOKEN
from config.settings import MONGODB_URI
import asyncio
import motor.motor_asyncio

handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents = intents, allowed_mentions=discord.AllowedMentions(roles=True, users=True, everyone=True))
discord.utils.setup_logging(handler=handler, level=logging.DEBUG, root=False)

@bot.event
async def on_ready():
  print(f'Logged on as {bot.user}!')
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='F1 | use /latest'))

async def load():
  # Load cogs
  for cog in ['test', 'results', 'scoreboard', 'predict']:
    await bot.load_extension(f'cogs.{cog}')

async def main():
  try:
    async with bot:
      await load()
      bot.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
      await bot.start(TOKEN)
  except asyncio.CancelledError:
    bot.mongoConnect.close()
    print("Main coroutine was cancelled.")

asyncio.run(main())