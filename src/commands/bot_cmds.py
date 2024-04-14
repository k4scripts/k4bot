import discord
from discord.ext import commands


class BotInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    bot = discord.SlashCommandGroup(
        "bot", "Bot related commands.")

    @bot.command(description='Gives info about the bot.')
    async def info(self, ctx: discord.ApplicationContext):

        embed = discord.Embed(
            description='''**k4bot** is made by the **k4scripts** development team.
                This bot is fully open-sourced. You can find the source-code of the bot on [our Github](https://github.com/k4scripts/). You're free to fork, contribute or use it as you please but we kindly ask you to respect the [MIT License](https://github.com/k4scripts/k4bot/tree/main?tab=MIT-1-ov-file).
                Thank you.''',
            color=discord.Color.from_rgb(0, 0, 0)
        )
        embed.set_footer(text='- K4oS, Founder k4scripts')
        embed.set_thumbnail(
            url='https://github.com/k4scripts/k4bot/blob/main/k4bot_logo.png?raw=true')

        await ctx.respond(embed=embed)


def setup(client):
    client.add_cog(BotInfo(client))
