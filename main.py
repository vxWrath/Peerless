import asyncio
import datetime
import os

import colorlog
import pytz
from dotenv import load_dotenv

load_dotenv()

from peerless import Bot, Cache, Database


class Formatter(colorlog.ColoredFormatter):
    def converter(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp=timestamp, tz=pytz.timezone('US/Central')).timetuple()
    
class DiscordHandler(colorlog.StreamHandler):
    def __init__(self, bot: Bot):
        super().__init__()
        
        self.bot = bot
        
    def handle(self, record) -> bool:
        if record.exc_info:
            self.bot.dispatch("error", "LOGGER", *record.exc_info)
            return True
        else:
            return super().handle(record)
    
async def main():
    token = os.getenv('TOKEN', '')
    bot   = Bot()

    colors = colorlog.default_log_colors | {"DEBUG": "white"}
    
    bot_handler   = colorlog.StreamHandler()
    bot_formatter = Formatter('%(log_color)s[%(asctime)s][BOT][%(levelname)s] %(message)s', datefmt='%m/%d/%Y %r', log_colors=colors | {"INFO": "bold_purple"})
    bot_logger    = colorlog.getLogger("bot")
    
    bot_handler.setFormatter(bot_formatter)
    bot_logger.addHandler(bot_handler)
    bot_logger.setLevel(colorlog.DEBUG)

    discord_handler   = DiscordHandler(bot)
    discord_formatter = Formatter(' %(log_color)s[%(asctime)s][DISCORD][%(levelname)s] %(message)s', datefmt='%m/%d/%Y %r', log_colors=colors | {"INFO": "black"})
    discord_logger    = colorlog.getLogger("discord")

    discord_handler.setFormatter(discord_formatter)
    discord_logger.addHandler(discord_handler)
    discord_logger.setLevel(colorlog.INFO)

    try:
        async with bot:
            bot.cache    = await Cache.create()
            bot.database = await Database.create(bot)

            await bot.start(token)
    except asyncio.CancelledError:
        pass
    finally:
        bot_logger.info("Turning Off...")

        await bot.cache.close()
        await bot.database.close()
        await bot.close()
            
        bot_logger.info("Turned Off")
        
if __name__ == '__main__':
    asyncio.run(main())