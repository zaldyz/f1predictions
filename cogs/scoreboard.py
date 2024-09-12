import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import fetchScores
from datetime import datetime

LEADERBOARD_LENGTH = 10

class Scoreboard(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Scoreboard cog loaded")

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    print(f"Joined a new guild: {guild.name} (ID: {guild.id})")
    await guild.create_role(name="Predictions", colour=discord.Colour(0xE8112D), mentionable=True)
    db = self.bot.mongoConnect["f1-predictions"]
    collection = db["scores"]
    try:
      await collection.insert_one({
        "guild_id": guild.id,
        "scoreboard": {},
        "latest_preds": [],
        "previous_preds": {},
      })
    except:
      print("A Database error has occured")
      

  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    print(f'Removed from guild {guild.name}')
    db = self.bot.mongoConnect["f1-predictions"]
    collection = db["scores"]
    try:
      await collection.delete_one({
        "guild_id": guild.id,
      })
    except:
      print("A Database error has occured")
  
  @app_commands.command(name="join")
  async def player_join(self, interaction: discord.Interaction):
    db = self.bot.mongoConnect["f1-predictions"]
    collection = db["scores"]

    result = await collection.update_one(
        {
          "guild_id": interaction.guild.id,
          f"scoreboard.{interaction.user.id}": {
            "$exists": False
          }
        },
        {
          "$set": {
            f"scoreboard.{interaction.user.id}": {
              # TODO: Might be better to use fetch_user on their id to
              # ensure display_name stays updated
              "display_name": interaction.user.display_name,
              "score": 0,
            }
          }
        }
    )
    message = ""
    if result.matched_count == 0:
      message = f"{interaction.user.mention} has already joined."
    elif result.modified_count == 0:
      message = "Something funky has happened, check logs"
    else:
      message = f"{interaction.user.mention} has successfully joined!"

    # TODO Create a helper function to check this
    role = discord.utils.get(interaction.guild.roles, name="Predictions")
    if not role:
      await interaction.guild.create_role(name="Predictions", colour=discord.Colour(0xE8112D), mentionable=True)
      role = discord.utils.get(interaction.guild.roles, name="Predictions")
    
    if role not in interaction.user.roles:
      await interaction.user.add_roles(role)
    await interaction.response.send_message(message, ephemeral=True)

  @app_commands.command(name="leaderboard")
  async def show_leaderboard(self, interaction: discord.Interaction):
    scores = await fetchScores(self.bot, interaction.guild.id)
    if not scores:
      await interaction.response.send_message("uh oh this is empty, join the game by using /join or by making your first /predict")
      return
    user_score = scores[str(interaction.user.id)]
    scores = [{"id": id, "display_name": value["display_name"], "score": value["score"]} for id, value in scores.items()]
    num_players = len(scores)
    scores.sort(key=lambda x: -int(x['score']))
    user_index = next((i for i, d in enumerate(scores) if d["id"] == str(interaction.user.id)), -1)
    scores = scores[:LEADERBOARD_LENGTH]

    embed = discord.Embed(
      colour=discord.Colour.red(),
      title=f"**Top {LEADERBOARD_LENGTH} Leaderboard**",
      timestamp=datetime.now()
    )
    embed.set_footer(text="You are not ranked yet.")
    embed.set_author(name="F1Predictions", icon_url=self.bot.user.avatar.url)
    if user_index > -1:
      embed.set_footer(text=f"@{interaction.user.display_name}, you are rank #{user_index + 1} of {num_players} with a score of {user_score['score']}")
    # for i, user in enumerate(scores):
      # desc += f"**{i + 1}. {user['display_name']}:** {user['score']} pts.\n"
    def format_leaderboard_entry(x):
      i, user = x
      return f"**{i + 1}. {user['display_name']}:** {user['score']} points"
    desc = list(map(format_leaderboard_entry, enumerate(scores)))
    desc = "\n".join(desc)
    embed.add_field(name="", value=desc, inline=False)
    await interaction.response.send_message(embed=embed)

async def setup(bot):
  await bot.add_cog(Scoreboard(bot))