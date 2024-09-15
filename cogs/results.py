import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from utils.openf1 import get_session_info
from utils.openf1 import get_session_results
from utils.ergast import get_constructor_standings, get_driver_standings
from utils.driver_info import display_position_str
from utils.driver_info import sessions
import pytz
from table2ascii import Alignment, table2ascii as t2a, PresetStyle


class Results(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Results cog loaded")

  @app_commands.command(name="latest", description="Get a real time update on the current or most recent session. :stopwatch:")
  async def latest(self, interaction: discord.Interaction):
    await interaction.response.defer()
    results = await get_session_results()

    positions = [f"{display_position_str[position['position']]:<4}: {position['driver_flag']} {position['driver_name']}" for position in results['positions']]
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


  @app_commands.command(name="results", description="Get results for any Practice, Qualifying, Sprint or Race session. :checkered_flag:")
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

    positions = [f"{display_position_str[position['position']]:<4}: {position['driver_flag']} {position['driver_name']}" for position in results['positions']]
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
  
  # @app_commands.command(name="schedule")
  # async def schedule(self, interaction: discord.Interaction):
  #   db = self.bot.mongoConnect['f1-predictions']
  #   collection = db['races']
  #   sessions = collection.find({})
  #   message = ""
  #   australian_tz = pytz.timezone('Australia/Sydney')
  #   async for session in sessions:
  #     # Convert the datetime object to the Australian time zone
  #     australian_time = session['date_start'].astimezone(australian_tz)

  #     # Format the time to a readable string
  #     formatted_time = australian_time.strftime('%B %d %I:%M %p')
  #     message += f"{formatted_time} {session['circuit']} {session['country']} {session['session_type']}\n"

  #   await interaction.response.send_message(f"`{message}`")
  @app_commands.command(name="driver_standings", description="Display the Driver Standings for any given season :military_medal:")
  @app_commands.describe(year="Select the season, providing none will automatically select current season")
  async def driver_standings(self, interaction: discord.Interaction, year: app_commands.Range[int, 1950, 2024] = 2024):
    await interaction.response.defer()
    standings = await get_driver_standings(year)
    if not standings:
      await interaction.followup.send("Data for that season couldn't be retrieved :(")
      return
    standings = standings[0]
    body = [[entry['position'], f"{entry['Driver']['givenName']} {entry['Driver']['familyName']}", entry['Constructors'][0]['name'], entry['wins'], entry['points']] for entry in standings['DriverStandings']]
    output = t2a(
      header=["Rank", "Driver", "Constructor", "Wins", "Points"],
      body=body,
      # first_col_heading=True
      style=PresetStyle.plain,
      cell_padding=0,
      alignments=Alignment.LEFT,
    )
    embed = discord.Embed(
      title=f"**Forumula 1 {year} Driver Standings :checkered_flag:**",
      description=f"```{output}```",
      timestamp=datetime.now(),
      colour=discord.Colour.gold()
    )
    embed.set_author(name="F1Predictions", icon_url=self.bot.user.avatar.url)
    await interaction.followup.send(embed=embed)
  
  @app_commands.command(name="constructor_standings", description="Display the Constructor Standings for any given season :bar_chart:")
  @app_commands.describe(year="Select the season, providing none will automatically select current season")
  async def constructor_standings(self, interaction: discord.Interaction, year: app_commands.Range[int, 1958, 2024] = 2024):
    await interaction.response.defer()
    standings = await get_constructor_standings(year)
    if not standings:
      await interaction.followup.send("Data for that season couldn't be retrieved :(")
      return
    standings = standings[0]
    body = [[entry['position'], entry['Constructor']['name'], entry['wins'], entry['points']] for entry in standings['ConstructorStandings']]
    output = t2a(
      header=["Rank", "Constructor", "Wins", "Points"],
      body=body,
      # first_col_heading=True
      style=PresetStyle.plain,
      cell_padding=0,
      alignments=Alignment.LEFT,
    )
    embed = discord.Embed(
      title=f"**Forumula 1 {year} Constructor Standings :race_car:**",
      description=f"```{output}```",
      timestamp=datetime.now(),
      colour=discord.Colour.dark_gold()
    )
    embed.set_author(name="F1Predictions", icon_url=self.bot.user.avatar.url)
    await interaction.followup.send(embed=embed)

async def setup(bot):
  await bot.add_cog(Results(bot))