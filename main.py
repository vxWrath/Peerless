import asyncio

from dotenv import load_dotenv

from peerless import Database, LeagueData, PlayerData, PlayerLeagueData, Team

load_dotenv()

async def main():
    db = await Database.create()

    print(await db.fetch_player(2, 1, keys="demands"))

asyncio.run(main())