# Embed helper functions
from config.settings import LEADERBOARD_LENGTH
from datetime import datetime
from config.settings import POINTS_CORRECT_P1, DISTANCE_TO_RECIEVE_POINTS, DISTANCE_POINTS, POINTS_CORRECT_TOP_3, POINTS_CORRECT_TOP_5, POINTS_CORRECT_TOP_10, POINTS_CORRECT_3_DRIVERS, POINTS_CORRECT_5_DRIVERS, POINTS_CORRECT_10_DRIVERS
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
    colour=discord.Colour.pink(),
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
  desc = list(map(format_leaderboard_entry, enumerate(sorted(leaderboard, key=lambda x: x['score'], reverse=True))))
  desc = "\n".join(desc)
  embed.add_field(name="", value=desc, inline=False)
  return embed

def create_rules_embed():
  embed = discord.Embed(
    title="**Rules :notepad_spiral:**",
    description="Use `/predict` to select your top 10 Drivers before the session starts.\nOnce the session ends, points will be awarded automatically to you based on any correct or close guesses.\nUse `/leaderboard` to view the scoreboard and view your score and rank.",
    color=discord.Color.greyple()
  )
  
  # Adding fields for the rules
  embed.add_field(name="**Correct Winner :trophy:**", value=f"Correctly guessing 1st place will grant you {POINTS_CORRECT_P1} points.", inline=False)
  embed.add_field(name="**Correct Position :white_check_mark:**", value="Correctly guessed positions towards the front of the grid will reward more points ", inline=False)
  embed.add_field(name="**Close Guesses :eyes:**", value=f"If a guess is within {DISTANCE_TO_RECIEVE_POINTS} places, you will recieve {DISTANCE_POINTS} point each.", inline=False)
  embed.add_field(name="**Top :three:, :five: and :keycap_ten:**", value=f"Correctly guessing the Top 3, 5 or all 10 positions in a row will grant you {POINTS_CORRECT_TOP_3}, {POINTS_CORRECT_TOP_5} and {POINTS_CORRECT_TOP_10} respectively.", inline=False)
  embed.add_field(name="**Correct :three:, :five: and :keycap_ten:**", value=f"If your top 3, 5 or 10 drivers are correct, but out of order, you will receive {POINTS_CORRECT_3_DRIVERS}, {POINTS_CORRECT_5_DRIVERS} and {POINTS_CORRECT_10_DRIVERS} respectively.", inline=False)

  # Footer and thumbnail
  # embed.set_footer(text="Loser at the end pays for everyone's cruise trip 💗")
  # embed.set_thumbnail(url="https://example.com/image.png")
  return embed