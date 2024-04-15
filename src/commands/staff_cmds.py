import os
import discord
from modules.logger import logger
from discord.ext import commands
from utils.embeds import DMEmbed, SuccessEmbed, WarningEmbed, ErrorEmbed


class StaffCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    staff = discord.SlashCommandGroup(
        "staff", "Staff commands.")

    @staff.command(description='Sends a DM to a user.')
    async def dm(self, ctx: discord.ApplicationContext, user: discord.Member, message:discord.Option(str, description='The message you want to send.')):

        if not isinstance(ctx.channel, discord.DMChannel):
            return await ctx.respond(WarningEmbed('This command can only be executed in a DM.'), ephemeral=True)

        staff_role_id = int(os.getenv('STAFF_ROLE_ID'))
        staff_role = ctx.guild.get_role(staff_role_id)
        
        if staff_role not in ctx.author.roles:
            return await ctx.respond(WarningEmbed('You do not have permission to use this command.'), ephemeral=True)
        
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label=f'Send from {ctx.author.guild.name}', disabled=True))
        
        try:
            await user.send(embed=DMEmbed(message, ctx.author, ctx.guild), view=view)
            await ctx.respond(embed=SuccessEmbed(f'Message sent to {user.mention} successfully.'), ephemeral=True)
        except Exception as e:
            logger.error(e)
            await ctx.respond(embed=ErrorEmbed(f'Failed to send message to {user.mention}.'), ephemeral=True)

def setup(client):
    client.add_cog(StaffCmds(client))
