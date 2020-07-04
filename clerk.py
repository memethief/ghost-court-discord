# Clerk cog
from discord.ext import commands
from ghostcourt import debug, debug_obj
from casequeue import CaseQueue
from rolequeue import RoleQueue

class ClerkCog(commands.Cog, name="Clerk commands"):
    def __init__(self, bot):
        self.bot = bot
        self.caseq = CaseQueue()
        self.roleq = RoleQueue()
        debug("Clerk cog started")

    @commands.has_role('Clerk')
    @commands.command(name='qcase')
    async def enqueue_case(self, ctx):
        '''
        Add a case to the docket

        This command will add a case to the queue, for an upcoming 
        hearing. Currently the case chosen is random.
        '''
        if self.caseq.choose():
            debug("successfully chose new case")
        else:
            debug("something went wrong")

        pass

    @commands.has_role('Clerk')
    @commands.command(name='lineup')
    async def rolequeue_lineup(self, ctx):
        '''
        View the lineup for the next case
        '''
        lineup = self.roleq.lineup()
        response = list()
        for role, member in lineup.items():
            if member is None:
                debug("{0}: {1}", role, member)
                response.append("{0}: (empty)".format(role))
            else:
                debug("{0}: {1}", role, member)
                response.append("{0}: {1}".format(role, member))

        await ctx.send("\n".join(response))
