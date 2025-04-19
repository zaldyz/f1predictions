import json
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://zaldy:7pfid7ZPbh9aWY6w@cluster1.dwj5j4y.mongodb.net/?retryWrites=true&w=majority")
db = client["f1-predictions"]  # Access database
collection = db["races"]  # Access collection

with open("schedule25.json", "r") as file:
  data = json.load(file)

  to_insert = [{
    "date_start": datetime.fromisoformat(session['start_date']),
    "circuit": session['circuit_name'],
    "country": session['country'],
    "session_type": session['session_type'],
  } for session in data]

  result = collection.insert_many(to_insert)

  print(result.inserted_ids)