# Clerk cog
from discord.ext import commands
import ghostcourt

class ClerkCog(commands.Cog, name="Clerk commands"):
    def __init__(self, bot):
        self.bot = bot
        ghostcourt.debug("Clerk cog started")
