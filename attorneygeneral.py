# Attorney General cog
from discord.ext import commands
import ghostcourt

class AttorneyGeneralCog(commands.Cog, name="Attorney General commands"):
    def __init__(self, bot):
        self.bot = bot
        ghostcourt.debug("AttorneyGeneral cog started")

    @commands.has_role('AttorneyGeneral')
    @commands.command(name='rebot')
    async def restart(self, ctx, user, *roles):
    	'''
    	Save state and restart the Ghost Court bot.
    	'''
    	pass
