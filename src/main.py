import os
import discord
from modules.logger import logger
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot(
    debug_guilds=[int(os.getenv('GUILD_ID'))], intents=discord.Intents.all())


@bot.event
async def on_ready():
    logger.info(f"{bot.user} is ready and online!")


def load_commands(exceptions: list[str] = []):
    ''' Loads all commands from the commands/ folder. '''
    CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

    for file_name in os.listdir(f'{CURRENT_PATH}/commands'):
        cog_name = file_name[:-3]
        if not file_name.endswith('.py') or cog_name in exceptions:
            continue

        try:
            bot.load_extension(f'commands.{cog_name}')
            logger.info(f'Command loaded: {cog_name}')

        except Exception as e:
            logger.warning(f'{type(e).__name__}: {e}')


if __name__ == '__main__':
    load_commands()
    bot.run(os.getenv('TOKEN'))
