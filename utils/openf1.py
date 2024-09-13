import aiohttp
import asyncio
from yarl import URL
from datetime import datetime
from .driver_info import drivers_2024
from .driver_info import driver_flags

positions_url = "https://api.openf1.org/v1/position"
session_url = "https://api.openf1.org/v1/sessions"

async def fetch(session, url):
  async with session.get(url) as response:
    return await response.json()

async def get_session_info(circuit_key, session_type, year):
  """Fetch session info for a particular circuit, session_type and year"""
  session = aiohttp.ClientSession()

  url_with_params = str(URL(session_url).with_query({"circuit_key": str(circuit_key), "session_name": session_type, "year": str(year)}))
  session_info = await fetch(session, url_with_params)

  await session.close()
  return session_info

async def get_session_results(session_key='latest'):
  """Fetch driver positions for a session"""        
  session = aiohttp.ClientSession()

  race_info, data = await asyncio.gather(
    fetch(session, str(URL(session_url).with_query({"session_key": session_key}))),
    fetch(session, str(URL(positions_url).with_query({"session_key": session_key})))
  )
  await session.close()

  positions = []

  # Sort by 'age' first, then by 'score'
  sorted_data = sorted(data, key=lambda x: (x['driver_number'], -datetime.fromisoformat(x['date']).timestamp()))

  seen = set()
  final_data = []
  for pos in sorted_data:
    if pos['driver_number'] not in seen:
        final_data.append({
           "driver_number": pos['driver_number'],
           "position": pos['position'],
           "driver_name" : drivers_2024[pos['driver_number']],
           "driver_flag": driver_flags[pos['driver_number']]
        })
        seen.add(pos['driver_number'])
  
  sorted_final = sorted(final_data, key=lambda x: x['position'])
  return {
    "info": race_info,
    "positions": sorted_final
  }