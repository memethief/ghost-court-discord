# Clerk cog
from discord.ext import commands
from ghostcourt import debug, debug_obj
from casequeue import CaseQueue

class ClerkCog(commands.Cog, name="Clerk commands"):
    def __init__(self, bot):
        self.bot = bot
        ghostcourt.debug("Clerk cog started")

    @commands.has_role('Clerk')
    @commands.command(name='qcase')
    async def enqueue_case(self, ctx):
    	'''
    	Add a case to the docket

    	This command will add a case to the queue, for an upcoming 
    	hearing. Currently the case chosen is random.
    	'''
        CaseQueue.choose()
    	pass
