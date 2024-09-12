import discord
from discord import app_commands
from discord.ext import commands

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
            f"scoreboard.{interaction.user.id}": 0
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

  
  

async def setup(bot):
  await bot.add_cog(Scoreboard(bot))