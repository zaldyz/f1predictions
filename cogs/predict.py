import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from utils.openf1 import get_session_info
from utils.openf1 import get_session_results
from utils.driver_info import display_position_str
from utils.driver_info import sessions
from utils.driver_info import drivers

class Predictions(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Predictions cog loaded")

  @app_commands.command(name="predict", description="Submit your prediction for the Top 10 Drivers!")
  @app_commands.describe(p1="Select your driver to finish P1")
  @app_commands.describe(p2="Select your driver to finish P2")
  @app_commands.describe(p3="Select your driver to finish P3")
  @app_commands.describe(p4="Select your driver to finish P4")
  @app_commands.describe(p5="Select your driver to finish P5")
  @app_commands.describe(p6="Select your driver to finish P6")
  @app_commands.describe(p7="Select your driver to finish P7")
  @app_commands.describe(p8="Select your driver to finish P8")
  @app_commands.describe(p9="Select your driver to finish P9")
  @app_commands.describe(p10="Select your driver to finish P10")
  @app_commands.choices(p1=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  @app_commands.choices(p2=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  @app_commands.choices(p3=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  @app_commands.choices(p4=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  @app_commands.choices(p5=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  @app_commands.choices(p6=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  @app_commands.choices(p7=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  @app_commands.choices(p8=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  @app_commands.choices(p9=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  @app_commands.choices(p10=
    [discord.app_commands.Choice(name=drivers[driver_num], value=driver_num) for driver_num in drivers])
  async def predict(interaction: discord.Interaction, p1: discord.app_commands.Choice[int], p2: discord.app_commands.Choice[int], p3: discord.app_commands.Choice[int], p4: discord.app_commands.Choice[int], p5: discord.app_commands.Choice[int], p6: discord.app_commands.Choice[int], p7: discord.app_commands.Choice[int], p8: discord.app_commands.Choice[int], p9: discord.app_commands.Choice[int], p10: discord.app_commands.Choice[int]):
      await interaction.response.send_message(f"{interaction.user.mention} has predicted: `🥇 P1: {p1.name}, 🥈 P2: {p2.name}, 🥉 P3: {p3.name}, P4: {p4.name}, P5: {p5.name}, P6: {p6.name}, P7: {p7.name}, P8: {p8.name}, P9: {p9.name}, P10: {p10.name}`")

async def setup(bot):
  await bot.add_cog(Predictions(bot))