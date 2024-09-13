import os

TOKEN = os.getenv("DISCORD_TOKEN")
MONGODB_URI = os.getenv("MONGODB_URI")

# Number of drivers to predict
NUM_DRIVERS_PREDICT = 10
# Number of players to be displayed on leaderboard
LEADERBOARD_LENGTH = 10