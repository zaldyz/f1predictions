
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

  