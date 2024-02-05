import discord
from utils.roblox_api import get_user_headshot_url


class ErrorEmbed(discord.Embed):
    ''' An error embed.'''

    def __init__(self, description: str):
        super().__init__(
            description=description,
            color=discord.Color.red()
        )


class WarningEmbed(discord.Embed):
    ''' A warning embed.'''

    def __init__(self, description: str):
        super().__init__(
            description=description,
            color=discord.Color.orange()
        )


class SuccessEmbed(discord.Embed):
    ''' A success embed.'''

    def __init__(self, description: str):
        super().__init__(
            description=description,
            color=discord.Color.green()
        )


class WhoIsEmbed(discord.Embed):
    ''' An embed for the WhoIs command.'''

    def __init__(self, data: dict):
        super().__init__(
            color=discord.Color.green()
        )

        def _format_name(roblox_data: dict) -> str:
            ''' Returns a formatted name. '''
            name_text = roblox_data['name']

            if 'displayName' in roblox_data:
                name_text += f' ({roblox_data["displayName"]})'

            return f'{name_text} - {roblox_data["id"]}'

        self.set_author(
            name=_format_name(data['roblox_profile']),
            icon_url=get_user_headshot_url(data['roblox_profile']['id']),
            url=f'https://www.roblox.com/users/{data["roblox_profile"]["id"]}/profile'
        )
        self.add_field(
            name='🌱 Created At',
            value=f'<t:{data["roblox_profile"]["created_at"]}>',
            inline=True
        )
        self.add_field(
            name='✅ Verified At',
            value=f'<t:{data["verified_at"]}>',
            inline=True
        )


class ValidationEmbed(discord.Embed):
    ''' An embed to promt the user to make sure.'''

    def __init__(self, description: str, title:str = 'Are you sure?'):
        super().__init__(
            title=title,
            description=description,
            color=discord.Color.orange()
        )
