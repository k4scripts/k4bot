import discord


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

