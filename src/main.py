import discord
import os
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot(debug_guilds=[int(os.getenv('GUILD_ID'))], intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

def load_extension(exceptions: list = []):
    ''' Loads all extensions from the extensions/ folder. '''
    CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

    for file_name in os.listdir(f'{CURRENT_PATH}/extensions'):
        cog_name = file_name[:-3]
        if not file_name.endswith('.py') or cog_name in exceptions:
            continue

        try:
            bot.load_extension(f'extensions.{cog_name}')
            print(f'Module loaded: {cog_name}')

        except Exception as e:
            print(f'{type(e).__name__}: {e}')

if __name__ == '__main__':
    load_extension()
    bot.run(os.getenv('TOKEN'))