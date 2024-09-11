import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from utils.openf1 import get_session_info
from utils.openf1 import get_session_results
from utils.driver_info import display_position_str
from utils.driver_info import sessions

class Results(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Results cog loaded")

  @app_commands.command(name="latest", description="Get a real time update on the current or most recent session.")
  async def latest(self, interaction: discord.Interaction):
    await interaction.response.defer()
    results = await get_session_results()
    print(results)

    positions = [f"{display_position_str[position['position']]:<4}: {position['driver_name']}" for position in results['positions']]
    order = "\n".join(positions)

    date_obj = datetime.fromisoformat(results['info'][0]['date_start'])

    embed = discord.Embed(
      colour=discord.Colour.red(),
      description=f"{results['info'][0]['location']}, {results['info'][0]['country_name']}", 
      title=f"{results['info'][0]['circuit_short_name']} {results['info'][0]['session_name']} Results",
      timestamp=datetime.now()
    )
    embed.add_field(name="", value=order, inline=False)
    embed.set_author(name="F1Predictions", icon_url=self.bot.user.avatar.url)
    embed.set_footer(text=f"Session Start: {date_obj.strftime("%B %d, %Y at %I:%M %p")}\n")
    await interaction.followup.send(f"{interaction.user.mention}, here are the latest session results.\n", embed=embed)


  @app_commands.command(name="results", description="Get results for any Practice, Qualifying, Sprint or Race session.")
  @app_commands.describe(circuit="Select the name of the circuit")
  @app_commands.describe(race_type="Select the session type")
  @app_commands.describe(year="Select the season, providing none will automatically select current season")
  @app_commands.choices(circuit=
    [discord.app_commands.Choice(name=sessions[circuit_key], value=circuit_key) for circuit_key in sessions])
  @app_commands.choices(race_type=
    [discord.app_commands.Choice(name="Sprint", value="Sprint"),
    discord.app_commands.Choice(name="Sprint Shootout", value="Sprint Shootout"),
    discord.app_commands.Choice(name="Race", value="Race"),
    discord.app_commands.Choice(name="Qualifying", value="Qualifying"),
    discord.app_commands.Choice(name="Practice 1", value="Practice 1"),
    discord.app_commands.Choice(name="Practice 2", value="Practice 2"),
    discord.app_commands.Choice(name="Practice 3", value="Practice 3"),
    ])
  async def results(self, interaction: discord.Interaction, circuit: discord.app_commands.Choice[str], race_type: discord.app_commands.Choice[str], year: int=2024):
    await interaction.response.defer()

    session_info = await get_session_info(circuit.value, race_type.value, year)
    if len(session_info) == 0:
      await interaction.followup.send(f"{interaction.user.mention}, No session found for those values :(.\n")
      return
      
    results = await get_session_results(session_info[0]['session_key'])

    positions = [f"{display_position_str[position['position']]:<4}: {position['driver_name']}" for position in results['positions']]
    order = "\n".join(positions)

    date_obj = datetime.fromisoformat(results['info'][0]['date_start'])

    embed = discord.Embed(
      colour=discord.Colour.red(),
      description=f"{results['info'][0]['location']}, {results['info'][0]['country_name']}", 
      title=f"{results['info'][0]['circuit_short_name']} {results['info'][0]['session_name']} Results",
      timestamp=datetime.now()
    )
    embed.add_field(name="", value=order, inline=False)
    embed.set_author(name="F1Predictions", icon_url=self.bot.user.avatar.url)
    embed.set_footer(text=f"Session Start: {date_obj.strftime("%B %d, %Y at %I:%M %p")}\n")
    await interaction.followup.send(f"{interaction.user.mention}, here are the session results.\n", embed=embed)

async def setup(bot):
  await bot.add_cog(Results(bot))