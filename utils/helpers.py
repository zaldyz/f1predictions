from datetime import datetime, timezone
from utils.points import points_per_position
from config.settings import DISTANCE_TO_RECIEVE_POINTS, DISTANCE_POINTS, POINTS_CORRECT_3_DRIVERS, POINTS_CORRECT_5_DRIVERS, POINTS_CORRECT_TOP_10, POINTS_CORRECT_TOP_3, POINTS_CORRECT_TOP_5, POINTS_CORRECT_10_DRIVERS

def time_until(target_time):
  now = datetime.now(timezone.utc)
  target = target_time.replace(tzinfo=timezone.utc)
  if target <= now:
    return "This session has already started"

  time_diff = target - now

  total_seconds = int(time_diff.total_seconds())
  hours = total_seconds // 3600
  minutes = (total_seconds % 3600) // 60

  if hours > 0:
    return f"{hours} hours and {minutes} minutes"
  else:
    return f"{minutes} minutes"
  
def filter_dict_lte_value(dict, value):
  """Filter the dict to only contain key, val pairs where val is less than or equal to value"""
  return {key: dict[key] for key in dict if dict[key] <= value}


def calculate_points(predictions, results):
  """Calculates the number of points to award for each prediction based on the final results"""
  scores = {}
  for user in predictions:
    user_preds = predictions[user]
    score = 0
    for driver_num in user_preds:
      if int(driver_num) not in results:
        continue
      if user_preds[driver_num] == results[int(driver_num)]:
        # Correct position guessed
        score += points_per_position[user_preds[driver_num]]
      elif abs(user_preds[driver_num] - results[int(driver_num)]) <= DISTANCE_TO_RECIEVE_POINTS:
        score += DISTANCE_POINTS
  
    # Check for correct top 10 drivers
    if user_preds == filter_dict_lte_value(results, 10):
      print("USER GUESSED ALL 10")
      score += POINTS_CORRECT_TOP_10
    elif sorted(map(lambda x: int(x), filter_dict_lte_value(user_preds, 10).keys())) == sorted(map(lambda x: int(x), filter_dict_lte_value(results, 10).keys())):
      print("USER GUESSED 10 DRIVERS BUT NOT ORDER")
      score += POINTS_CORRECT_10_DRIVERS
    elif filter_dict_lte_value(user_preds, 5) == filter_dict_lte_value(results, 5):
      print("USER GUESSED TOP 5")
      score += POINTS_CORRECT_TOP_5
    elif sorted(map(lambda x: int(x), filter_dict_lte_value(user_preds, 5).keys())) == sorted(map(lambda x: int(x), filter_dict_lte_value(results, 5).keys())):
      print("USER GUESSED 5 DRIVERS BUT NOT ORDER")
      score += POINTS_CORRECT_5_DRIVERS
    elif filter_dict_lte_value(user_preds, 3) == filter_dict_lte_value(results, 3):
      print("USER GUESSED TOP 3")
      score += POINTS_CORRECT_TOP_3
    elif sorted(map(lambda x: int(x), filter_dict_lte_value(user_preds, 3).keys())) == sorted(map(lambda x: int(x), filter_dict_lte_value(results, 3).keys())):
      print("USER GUESSED 3 DRIVERS BUT NOT ORDER")
      score += POINTS_CORRECT_3_DRIVERS
    scores[user] = score

  
  return scores




  