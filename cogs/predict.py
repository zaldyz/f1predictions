import discord
from discord import app_commands
from discord.ext import commands
from mongo.helpers import addPlayerToScoreboard, awardScoreBoardPoints, getLatestPredictions, getMostRecentSession, submitPrediction, getNextRaceInfo
from utils.driver_info import drivers, driver_flags, display_position_str
from config.settings import NUM_DRIVERS_PREDICT
from utils.helpers import calculate_points, time_until
from datetime import datetime
from utils.openf1 import get_session_results
from utils.embed import create_round_end_scoreboard

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
  async def predict(self, interaction: discord.Interaction, p1: discord.app_commands.Choice[int], p2: discord.app_commands.Choice[int], p3: discord.app_commands.Choice[int], p4: discord.app_commands.Choice[int], p5: discord.app_commands.Choice[int], p6: discord.app_commands.Choice[int], p7: discord.app_commands.Choice[int], p8: discord.app_commands.Choice[int], p9: discord.app_commands.Choice[int], p10: discord.app_commands.Choice[int]):

    await addPlayerToScoreboard(self.bot, interaction.guild.id, interaction.user)
    # TODO Create a helper function to check this
    role = discord.utils.get(interaction.guild.roles, name="Predictions")
    if not role:
      await interaction.guild.create_role(name="Predictions", colour=discord.Colour(0xE8112D), mentionable=True)
      role = discord.utils.get(interaction.guild.roles, name="Predictions")
    
    if role not in interaction.user.roles:
      await interaction.user.add_roles(role)

    guesses = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]

    if len(set([pos.value for pos in guesses])) != NUM_DRIVERS_PREDICT:
      await interaction.response.send_message("Error submitting your prediction :warning:, You cannot predict the same driver in more than one position.", ephemeral=True)
      return
    
    guesses_to_submit = {str(guess.value): position + 1 for position, guess in enumerate(guesses)}
    await submitPrediction(self.bot, interaction.guild.id, interaction.user.id, guesses_to_submit)
    order = [f"{display_position_str[position + 1]:<4}: {driver_flags[guess.value]} {drivers[guess.value]}" for position, guess in enumerate(guesses)]
    order = "\n".join(order)
    # Push the predictions to latest predictions
    next_session_info = await getNextRaceInfo(self.bot)
    
    embed = discord.Embed(
      colour=discord.Colour.blurple(),
      description=f"{next_session_info['circuit']}, {next_session_info['country']}", 
      title=f"{interaction.user.display_name}'s Top {NUM_DRIVERS_PREDICT} Prediction for {next_session_info['circuit']} {next_session_info['session_type']}",
      timestamp=datetime.now()
    )
    embed.add_field(name="", value=order, inline=False)
    embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
    embed.set_footer(text=f"Session Starts in: {time_until(next_session_info['date_start'])}")
    await interaction.response.send_message(embed=embed)
  
  @app_commands.command(name="remind", description="Send a reminder to players of the time until the next session starts")
  async def remind(self, interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name="Predictions")
    if not role:
      await interaction.guild.create_role(name="Predictions", colour=discord.Colour(0xE8112D))
      role = discord.utils.get(interaction.guild.roles, name="Predictions")
    next_session_info = await getNextRaceInfo(self.bot)
    await interaction.response.send_message(f"{role.mention} The next upcoming session **{next_session_info['circuit']}, {next_session_info['country']}: {next_session_info['session_type']}** starts in **{time_until(next_session_info['date_start'])}**.\n Use `/predict` to make your Top 10 prediction before the session starts!")
  
  @app_commands.command(name="end_session", description=":warning: Please DO NOT use this, let me use it only for now")
  async def end_session(self, interaction: discord.Interaction):
    # Defer here
    await interaction.response.defer()

    # Go to races, find the most recently finished race, delete it but get its info
    finished_session = await getMostRecentSession(self.bot)
    if not finished_session:
      await interaction.response.send_message("Error finishing session :warning: There are no recently finished sessions")
      return
    
    # Fetch latest session results
    results = await get_session_results()
    positions = {x['driver_number']: x['position'] for x in results['positions']}

    # Calculate the points for each user that guessed
    latest_preds = await getLatestPredictions(self.bot, interaction.guild.id)

    print(positions)
    print(latest_preds)
    points_to_award = calculate_points(latest_preds, positions)

    print(points_to_award)
    await awardScoreBoardPoints(self.bot, interaction.guild.id, points_to_award, latest_preds)

    # Go To Latest_preds, go and award points for all guesses by comparing the results and the guesses
    # Update the scoreboard with the added points, and delete latest_preds, and move it to previous preds

    # Create an embed with a leaderboard of the highest scorers for the session
    embed = await create_round_end_scoreboard(self.bot, points_to_award, finished_session['circuit'], finished_session['country'], finished_session['session_type'])

    role = discord.utils.get(interaction.guild.roles, name="Predictions")
    if not role:
      await interaction.guild.create_role(name="Predictions", colour=discord.Colour(0xE8112D), mentionable=True)
      role = discord.utils.get(interaction.guild.roles, name="Predictions")

    # await interaction.channel.send("hello")
    await interaction.followup.send(f"{role.mention}", embed=embed)

async def setup(bot):
  await bot.add_cog(Predictions(bot))