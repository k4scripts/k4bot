import os
import discord
from discord import Option, ApplicationContext
from discord.ext import commands

from utils.database import clear_db, remove_member_from_db
from utils.embeds import ErrorEmbed, ValidationEmbed, SuccessEmbed
from discord.ui import View, Button


class Database(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    database = discord.SlashCommandGroup(
        "database", "Database related commands.")

    @database.command(description='Clear the database.')
    async def clear(self, ctx: ApplicationContext):
        
        owner_id = int(os.getenv('OWNER_ID', 0))
        if ctx.author.id != owner_id:
            return await ctx.respond(embed=ErrorEmbed('You do not have permission to use this command.'), ephemeral=True)

        view = View()
        continue_button = Button(
            label='Continue', custom_id='continue', style=discord.ButtonStyle.red, emoji='🗑')

        cancel_button = Button(label='Cancel', custom_id='cancel',
                               style=discord.ButtonStyle.green, emoji='❌')

        async def cancel_callback(interaction: discord.Interaction):
            ''' Cancel the operation. '''
            await interaction.response.edit_message(embed=SuccessEmbed('Operation cancelled.'), view=None)

        async def continue_callback(interaction: discord.Interaction):
            ''' Continue with the operation. '''
            clear_db(interaction.user.id)
            await interaction.response.edit_message(embed=SuccessEmbed('Database has been erased.'), view=None)

        cancel_button.callback = cancel_callback
        continue_button.callback = continue_callback

        view.add_item(cancel_button)
        view.add_item(continue_button)

        await ctx.respond(embed=ValidationEmbed(f'Are you sure you want to erase the database?', ':warning: You\'re about to __ERASE__ the database :warning:'), view=view, ephemeral=True)

    @database.command(description='Remove user from the database.')
    async def remove(self, ctx: ApplicationContext, member: Option(discord.Member, description='The member to remove from the database.', required=True)):

        if not ctx.author.guild_permissions.administrator:
            return await ctx.respond(embed=ErrorEmbed('You do not have permission to use this command.'), ephemeral=True)

        if not remove_member_from_db(member.id):
            return await ctx.respond(embed=ErrorEmbed('This member is not in the database.'), ephemeral=True)

        await ctx.respond(embed=SuccessEmbed(f'{member.mention} has been removed from the database.'), ephemeral=True)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        remove_member_from_db(member.id)


def setup(client):
    client.add_cog(Database(client))
