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
    @commands.command(name='nextcase')
    async def next_case(self, ctx):
        '''
        Go to the next case

        This command will end the current case (if any) and attempt
        to start the next one. If any roles are vacant, the next 
        case will fail to load.
        '''
        response = list()
        lineup = self.roleq.lineup()
        missing = list()
        # Check to make sure all roles are assigned
        for role, member in lineup.items():
            if member is None:
                missing.append(role)
        if len(missing) == 0:
            # Send back an error
            response.append("Cannot start the next case. Must add "
                "members to the following role(s):")
            response.append(", ".join(missing))
            await ctx.send("\n".join(status))
            return

        # if there is a current case, archive it
        if not self.caseq.current is None:
            self.caseq.history.append(self.caseq.current)
            self.caseq.current = None

        # if we have cases on the docket, make the next one current
        if self.caseq.choose():
            debug("successfully chose new case")
        else:
            debug("something went wrong")

        pass

    @commands.has_role('Clerk')
    @commands.command(name='status')
    async def casequeue_status(self, ctx):
        '''
        View the status of cases
        '''
        status = list()
        for statline in self.caseq.status():
            status.append(statline)

        await ctx.send("\n".join(status))

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
