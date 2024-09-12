
async def fetchScores(bot, guild_id):
  """Fetch the scores for a given guild"""
  db = bot.mongoConnect["f1-predictions"]
  collection = db["scores"]
  try:
    document = await collection.find_one({"guild_id": guild_id})
  except:
    print('Error Fetching scoreboard: The guild was not found')
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
  except:
    print("A Database error has occured")

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