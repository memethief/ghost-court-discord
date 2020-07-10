# Clerk cog
from discord.ext import commands
from ghostcourt import debug, debug_obj, message_roles
from casequeue import CaseQueue
from rolequeue import RoleQueue
from court import Court, CourtState

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
    @commands.command(name='next')
    async def next(self, ctx):
        '''
        Progress to the next stage of the game. 

        The only reason this might fail is if we are trying to load the next 
        case and there is a vacant role.
        '''
        debug("Current state is {0}", Court.state.name)

        if Court.state == CourtState.WAITING:
            # We want to make sure that no roles are empty, so we can load a case
            missing = list()
            for role, member in self.roleq.lineup().items():
                if member is None:
                    missing.append(role)
            if len(missing) > 0:
                # send back an error message
                response = list()
                response.append("Cannot start the next case. Must add "
                    "player(s) to the following role(s):")
                response.append(", ".join(missing))
                await ctx.send("\n".join(response))
                return

        # If all is well, progress to the next state
        await self.state_cleanup(ctx)
        Court.next()
        await self.state_setup(ctx)

        debug("New state is {0}", Court.state.name)

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
            await ctx.send("\n".join(response))
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

    async def state_cleanup(self, ctx):
        '''
        Perform any operations required to clean up after the current court state
        '''
        debug("cleaning up after state: {0}", Court.state.name)

        if Court.state == CourtState.PLAINTIFF:
            # Stop plaintiff timer without notification
            pass
        elif Court.state == CourtState.DEFENDANT:
            # Stop defendant timer without notification
            pass
        elif Court.state == CourtState.JUDGE:
            # Stop judge timer without notification
            pass
        elif Court.state == CourtState.CLOSED:
            # Archive case
            pass

        pass

    async def state_setup(self, ctx):
        '''
        Perform any initial operations required for the current court state
        '''
        debug("setting up for state: {0}", Court.state.name)
        await message_roles(ctx, "setting up for state: {0}".format(Court.state.name), ['Clerk', 'Bailiff'])

        if Court.state == CourtState.WAITING:
            # Notify clerk
            await message_roles(ctx, "Ghost Court waiting for signups", ['Clerk'])
            pass
        elif Court.state == CourtState.ACTIVE:
            # Set current active case
            # Assign roles
            # Notify all
            await message_roles(ctx, "Case active; details forthcoming", ['Clerk'])
            pass
        elif Court.state == CourtState.PLAINTIFF:
            # Notify plaintiff and judge
            pass
        elif Court.state == CourtState.DEFENDANT:
            # Notify defendant and judge
            pass
        elif Court.state == CourtState.JUDGE:
            # Notify judge
            pass
        elif Court.state == CourtState.CLOSED:
            # Notify reporter
            pass

        await message_roles(ctx, "finished setup for {0}".format(Court.state.name), ['Clerk', 'Bailiff'])
        pass
