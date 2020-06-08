# General user cog
from discord.ext import commands
from ghostcourt import debug, debug_obj
from rolequeue import RoleQueue
from casequeue import CaseQueue

class UserCog(commands.Cog, name="Commands"):
    '''
    Commands available to all players

    These commands involve querying and manipulating the
    role queues.
    '''
    def __init__(self, bot):
        self.bot = bot
        self.rq = RoleQueue()
        debug("User cog started")

    @commands.command(name='cq')
    async def list_queue(self, ctx, *roles):
        '''
        List contents of queues

        By default, list all active queues you have joined.
        This will include information about how many people
        are ahead of you.

        If you want to see the complete queue for one or more
        roles, include the role name(s) after the command,
        separated by spaces. For example, to see the Judge and
        Clerk queues, you can enter the following:

            !cq judge clerk

        You may also use aggregate role names here.
        '''
        print('cq', flush=True)
        debug('listing queues with roles:')
        debug_obj(roles)

        msg_response = list()

        try:
            if len(roles) == 0:
                debug("zero args -- listing for user {0}", ctx.author)
                msg_response.append(self.rq.list_user(ctx.author))

            else:
                debug("{0} args", len(roles))
                msg_response = self.rq.list(roles)

        except Exception as e:
            debug("Whoops...")
            debug_obj(e)

        for msg in msg_response:
            debug("sending message...")
            await ctx.send(msg)

    @commands.command(name='q')
    async def enqueue(self, ctx, *roles):
        '''
        Add yourself to a queue or queues
        
        By itself this command will add you to all queues. You
        can limit this to specific queues by following the
        command with one or more role names. For example, if
        you want to be added only to the plaintiff and clerk
        queues, you may type:

            !q plaintiff clerk

        You may also use aggregate role names here.

        Note that this command does not affect your current
        place in any queues you have already joined. If you
        want to move to the back of a queue you must use !dq,
        followed by !q.
        '''
        debug('Got request to enqueue for {0}', roles)
        user = ctx.author
        self.rq.add(user, roles)
        await ctx.send(self.rq.list_user(user))

    @commands.command(name='dq')
    async def dequeue(self, ctx, *roles):
        '''
        Remove yourself from a queue or queues
        
        By itself this command will remove you from all queues.
        You can limit this to specific queues by following the
        command with one or more role names. For example, if
        you want to be removed from the defendant and reporter
        queues but keep your place in all other queues, you may
        type:

            !dq defendant reporter

        You may also use aggregate role names here.
        '''
        debug('Got request to dequeue from {0}', roles)
        user = ctx.author
        self.rq.remove(user, roles)
        await ctx.send(self.rq.list_user(user))

    @commands.command(name='showcase')
    async def showcase(self, ctx):
        '''
        Show case details

        This command displays the description of the current case,
        including the names of the litigants. Additional information
        is displayed for certain roles.

        Clerk: display description for the upcoming case as well.

        Current Plaintiff/Defendant: display your side of the story.

        Upcoming Plaintiff/Defendant: display your information for 
        the upcoming case.
        '''
        debug('Got request to show case information')
        case = CaseQueue().current
        if case is None:
            await ctx.send("No current case")
        else:
            await ctx.send("{0}\n{1}".format(case.title, case.summary))
        # check user.permissions_in(channel) for roles?
        # Want to use user.dm_channel to send response
        # Or maybe user.send() ?
        
        #await ctx.send(summary)

# Other methods

def format_queue(q):
    '''
    Given a queue object, return a string representation of it 
    suitable for a message in Discord
    '''
    pass

