import discord
from discord import Option, ApplicationContext
from discord.ext import commands

from utils.database import get_member_from_db
from utils.embeds import ErrorEmbed, WhoIsEmbed


class WhoIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Identifies a Discord user with their Roblox account.')
    async def whois(self,
                     ctx: ApplicationContext,
                     user: Option(discord.Member, description='The Discord user to identify', required=True),
                     ):

        data = get_member_from_db(user.id)
        if not data:
            await ctx.respond(embed=ErrorEmbed(f'Unable to find user. User is not verified?'), ephemeral=True)
            return
        
        await ctx.respond(embed=WhoIsEmbed(data))


def setup(client):
    client.add_cog(WhoIs(client))
