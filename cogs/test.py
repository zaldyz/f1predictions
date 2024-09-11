import discord
from discord import app_commands
from discord.ext import commands

class Slash(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
      print("Slash cog loaded")

  @app_commands.command(name="slash", description="test slash command")
  async def ping(self, interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong!")

async def setup(bot):
  await bot.add_cog(Slash(bot))