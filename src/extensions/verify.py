import discord
import string
import random
import re
import os
from utils.embeds import ErrorEmbed, SuccessEmbed, WarningEmbed
from utils.database import add_member_to_db
from discord import Option, ApplicationContext
from discord.ext import commands
from utils.roblox_api import get_profile
from discord.ui import View, Button


class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Verify with your Roblox account!')
    async def verify(self,
                     ctx: ApplicationContext,
                     user_id: Option(int, description='Your Roblox user ID', required=True),
                     ):

        verified_role_id = os.getenv('VERIFY_ROLE_ID', None)
        if not verified_role_id:
            await ctx.respond(embed=ErrorEmbed('The bot owner has not set the verified role ID.'), ephemeral=True)
            return

        verified_role = discord.utils.get(
            ctx.guild.roles, id=int(verified_role_id))
        if not verified_role:
            await ctx.respond(embed=ErrorEmbed('The verified role ID is invalid.'), ephemeral=True)
            return

        if verified_role in ctx.author.roles:
            await ctx.respond(embed=ErrorEmbed('You are already verified!'), ephemeral=True)
            return

        profile_data = get_profile(user_id)
        if not profile_data:
            await ctx.respond(embed=ErrorEmbed(f'User {user_id} does not exist.'), ephemeral=True)
            return

        view = View()

        verify_button = Button(
            label='Verify', custom_id='verify', style=discord.ButtonStyle.green, emoji='✅')
        regen_button = Button(label='Regenerate', custom_id='regen',
                              style=discord.ButtonStyle.blurple, emoji='🔄')

        async def regen_callback(interaction: discord.Interaction):
            ''' Regenerate the random string. '''
            random_string = ''.join(random.choice(
                string.ascii_letters) for _ in range(4))
            await interaction.response.edit_message(embed=SuccessEmbed(f'Please set your profile description to `{random_string}` and click the verify button.'), view=view)

        regen_button.callback = regen_callback

        async def verify_callback(interaction: discord.Interaction):

            verify_button.disabled = True
            regen_button.disabled = True

            profile_data = get_profile(user_id)
            if not get_profile(user_id):
                await interaction.response.edit_message(embed=ErrorEmbed(f'User {user_id} does not exist.'), view=view)
                return

            profile_description = profile_data.get('description', '')
            random_string = re.search(
                r'`([a-zA-Z]+)`', interaction.message.embeds[0].description).group(1)

            if random_string in profile_description:
                view.clear_items()
                await interaction.response.edit_message(embed=SuccessEmbed('You have been verified!'), view=view)
                try:
                    await ctx.author.add_roles(verified_role)
                except discord.Forbidden:
                    await ctx.respond(embed=ErrorEmbed('The bot does not have permission to add roles.'), ephemeral=True)

                name = profile_data.get('name', 'Unknown')

                try:
                    await ctx.author.edit(nick=name)
                except discord.Forbidden:
                    pass
                    #await ctx.respond(embed=ErrorEmbed('The bot does not have permission to edit your nickname.'), ephemeral=True)
                
                add_member_to_db(ctx.author.id, profile_data)

            else:
                verify_button.disabled = False
                regen_button.disabled = False

                await interaction.response.edit_message(embed=WarningEmbed(f'Please set your profile description to `{random_string}` and click the verify button.'), view=view)

        verify_button.callback = verify_callback

        view.add_item(verify_button)
        view.add_item(regen_button)

        random_string = ''.join(random.choice(
            string.ascii_letters) for _ in range(4))
        await ctx.respond(embed=SuccessEmbed(f'Please set your profile description to `{random_string}` and click the verify button.'), view=view, ephemeral=True)


def setup(client):
    client.add_cog(Verify(client))
