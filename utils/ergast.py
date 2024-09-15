import aiohttp
import asyncio

async def fetch(session, url):
  async with session.get(url) as response:
    return await response.json()


async def get_driver_standings(year="current"):
  """Fetch the driver standings for a given year"""
  session = aiohttp.ClientSession()

  url = f"http://ergast.com/api/f1/{year}/driverStandings.json"
  standings = await fetch(session, url)

  await session.close()
  return standings["MRData"]["StandingsTable"]["StandingsLists"]


async def get_constructor_standings(year="current"):
  """Fetch the constructors standings for a given year"""
  session = aiohttp.ClientSession()

  url = f"https://ergast.com/api/f1/{year}/constructorStandings.json"
  standings = await fetch(session, url)

  await session.close()
  return standings["MRData"]["StandingsTable"]["StandingsLists"]


