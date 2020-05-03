# General user cog
from discord.ext import commands

class UserCog(commands.Cog, name="Commands"):
    '''
    Commands available to all players

    These commands involve querying and manipulating the
    role queues.
    '''
    def __init__(self, bot):
        self.bot = bot
