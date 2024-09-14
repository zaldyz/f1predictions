import discord
from discord import app_commands
from discord.ext import commands
from mongo.helpers import addPlayerToScoreboard, fetchScores
from mongo.helpers import insertNewGuild
from mongo.helpers import removeGuild
from config.settings import LEADERBOARD_LENGTH
from datetime import datetime
from utils.embed import create_empty_scoreboard

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
    await insertNewGuild(self.bot, guild.id)
      
  @commands.Cog.listener()
  async def on_guild_remove(self, guild):
    print(f'Removed from guild {guild.name}')
    await removeGuild(self.bot, guild.id)
  
  @app_commands.command(name="join", description="Join the game to recieve notifications of upcoming races")
  async def player_join(self, interaction: discord.Interaction):
    message = await addPlayerToScoreboard(self.bot, interaction.guild.id, interaction.user)

    # TODO Create a helper function to check this
    role = discord.utils.get(interaction.guild.roles, name="Predictions")
    if not role:
      await interaction.guild.create_role(name="Predictions", colour=discord.Colour(0xE8112D), mentionable=True)
      role = discord.utils.get(interaction.guild.roles, name="Predictions")
    
    if role not in interaction.user.roles:
      await interaction.user.add_roles(role)
    await interaction.response.send_message(message, ephemeral=True)

  @app_commands.command(name="leaderboard", description="Display the leaderboard of players and their current scores")
  async def show_leaderboard(self, interaction: discord.Interaction):
    scores = await fetchScores(self.bot, interaction.guild.id)
    if not scores:
      await interaction.response.send_message(embed=create_empty_scoreboard(self.bot))
      return
    user_score = scores[str(interaction.user.id)]
    scores = [{"id": id, "display_name": value["display_name"], "score": value["score"]} for id, value in scores.items()]
    num_players = len(scores)
    scores.sort(key=lambda x: -int(x['score']))
    user_index = next((i for i, d in enumerate(scores) if d["id"] == str(interaction.user.id)), -1)
    scores = scores[:LEADERBOARD_LENGTH]

    embed = discord.Embed(
      colour=discord.Colour.yellow(),
      title=f"**Top {LEADERBOARD_LENGTH} Leaderboard** :trophy:",
      timestamp=datetime.now()
    )
    embed.set_footer(text="You are not ranked yet.")
    embed.set_author(name="F1Predictions", icon_url=self.bot.user.avatar.url)
    if user_index > -1:
      embed.set_footer(text=f"@{interaction.user.display_name}, you are rank #{user_index + 1} of {num_players} with a score of {user_score['score']}")
    def format_leaderboard_entry(x):
      i, user = x
      return f"{i + 1}. **{user['display_name']}**: **{user['score']}** points"
    desc = list(map(format_leaderboard_entry, enumerate(scores)))
    desc = "\n".join(desc)
    embed.add_field(name="", value=desc, inline=False)
    await interaction.response.send_message(embed=embed)

async def setup(bot):
  await bot.add_cog(Scoreboard(bot))