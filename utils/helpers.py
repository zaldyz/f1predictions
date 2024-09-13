
from datetime import datetime
def time_until(target_time):
  now = datetime.now()
  if target_time <= now:
    return "This session has already started"

  time_diff = target_time - now

  total_seconds = int(time_diff.total_seconds())
  hours = total_seconds // 3600
  minutes = (total_seconds % 3600) // 60

  if hours > 0:
    return f"{hours} hours and {minutes} minutes"
  else:
    return f"{minutes} minutes"