# Embed helper functions
from config.settings import LEADERBOARD_LENGTH
from datetime import datetime
import discord

def create_empty_scoreboard(bot):
  embed = discord.Embed(
    colour=discord.Colour.yellow(),
    title=f"**Top {LEADERBOARD_LENGTH} Leaderboard**",
    timestamp=datetime.now()
  )
  embed.set_footer(text="You are not ranked yet.")
  embed.set_author(name="F1Predictions", icon_url=bot.user.avatar.url)
  embed.add_field(name="Uh oh!", value="It appears no players have joined the game yet :slight_frown:\n Use `/join` to join the game and get notified for upcoming sessions or use `/predict` to make your first prediction!", inline=False)
  return embed

async def create_round_end_scoreboard(bot, points_awarded, circuit, country, session_type):
  embed = discord.Embed(
    colour=discord.Colour.yellow(),
    title=f"{circuit}, {country}: {session_type} has Ended :tada:",
    description="Points have been awarded! Here are the top scorers for this round:",
    timestamp=datetime.now()
  )
  leaderboard = []
  for user_id in points_awarded:
    user = await bot.fetch_user(user_id)
    leaderboard.append({"display_name": user.display_name, "score": points_awarded[user_id]})
  embed.set_author(name="F1Predictions", icon_url=bot.user.avatar.url)
  def format_leaderboard_entry(x):
    i, user = x
    return f"{i + 1}. **{user['display_name']}**: **{user['score']}** points"
  desc = list(map(format_leaderboard_entry, enumerate(sorted(leaderboard, key=lambda x: x['score']))))
  desc = "\n".join(desc)
  embed.add_field(name="", value=desc, inline=False)
  return embed