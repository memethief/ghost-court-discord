# Clerk cog
from discord.ext import commands

class ClerkCog(commands.Cog, name="Clerk commands"):
    def __init__(self, bot):
        self.bot = bot
