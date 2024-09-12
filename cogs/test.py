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

    db = self.bot.mongoConnect["f1-predictions"]
    collection = db["scores"]
    res = await collection.find_one({})
    await interaction.response.send_message(repr(res))

  @app_commands.command(name="role")
  async def create_role(self, interaction: discord.Interaction):
    # TODO Create a helper function to check this
    role = discord.utils.get(interaction.guild.roles, name="Predictions")
    created = False
    if not role:
      await interaction.guild.create_role(name="Predictions", colour=discord.Colour(0xE8112D), mentionable=True)
      role = discord.utils.get(interaction.guild.roles, name="Predictions")
      created = True
    
    added = False
    if role not in interaction.user.roles:
      await interaction.user.add_roles(role)
      added = True
    # await interaction.message.author.add_roles(role)
    await interaction.response.send_message(f"Role created: {created} Role added: {added}")
  
  @app_commands.command(name="remind")
  async def remind(self, interaction: discord.Interaction):
    role = discord.utils.get(interaction.guild.roles, name="Predictions")
    if not role:
      await interaction.guild.create_role(name="Predictions", colour=discord.Colour(0xE8112D))
      role = discord.utils.get(interaction.guild.roles, name="Predictions")
    await interaction.response.send_message(f"{role.mention} ALERT HEHEH")

  @app_commands.command(name="members")
  async def members(self, interaction: discord.Interaction):
    guild = interaction.guild
    members = [f"{member.name} {member.discriminator}" for member in guild.members]
    await interaction.response.send_message(repr(members[1]))

async def setup(bot):
  await bot.add_cog(Slash(bot))