
from datetime import datetime

async def fetchScores(bot, guild_id):
  """Fetch the scores for a given guild"""
  db = bot.mongoConnect["f1-predictions"]
  collection = db["scores"]
  try:
    document = await collection.find_one({"guild_id": guild_id})
  except Exception as e:
    print(f'Error Fetching scoreboard: {e}')
    return {}
  return document['scoreboard']

async def insertNewGuild(bot, guild_id):
  """Insert a document to represent a new guild"""
  db = bot.mongoConnect["f1-predictions"]
  collection = db["scores"]
  try:
    await collection.insert_one({
      "guild_id": guild_id,
      "scoreboard": {},
      "latest_preds": {},
      "previous_preds": {},
    })
  except:
    print("A Database error has occured")

async def removeGuild(bot, guild_id):
  """Delete a document representing a guild"""
  db = bot.mongoConnect["f1-predictions"]
  collection = db["scores"]
  try:
    await collection.delete_one({
      "guild_id": guild_id,
    })
  except Exception as e:
    print(f"a Database error has occured: {e}")

async def addPlayerToScoreboard(bot, guild_id, user):
  """Updates the guild document to add a new player to the scoreboard with a score of 0"""
  db = bot.mongoConnect["f1-predictions"]
  collection = db["scores"]

  result = await collection.update_one(
      {
        "guild_id": guild_id,
        f"scoreboard.{user.id}": {
          "$exists": False
        }
      },
      {
        "$set": {
          f"scoreboard.{user.id}": {
            # TODO: Might be better to use fetch_user on their id to
            # ensure display_name stays updated
            "display_name": user.display_name,
            "score": 0,
          }
        }
      }
  )
  if result.matched_count == 0:
    return f"{user.mention} has already joined."
  elif result.modified_count == 0:
    return "Something funky has happened, check logs"
  else:
    return f"{user.mention} has successfully joined!"
  

async def submitPrediction(bot, guild_id, user_id, guesses):
  """Submit latest prediction by a user for upcoming session"""
  db = bot.mongoConnect["f1-predictions"]
  collection = db["scores"]
  try:
    await collection.update_one(
      {
        "guild_id": guild_id,
      },
      {
        "$set": {
          f"latest_preds.{user_id}": guesses
        }
      }
    )
  except Exception as e:
    print(f"a Database error has occured: {e}")

async def getNextRaceInfo(bot):
  """Fetches the next upcoming Sprint Shootout, Sprint, Qualifying or Race session info"""
  now = datetime.now()
  db = bot.mongoConnect['f1-predictions']
  collection = db['races']
  closest = await collection.find({"date_start": {"$gt": now}}).sort("date_start", 1).limit(1).next()
  return closest