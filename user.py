# General user cog
from discord.ext import commands
import ghostcourt

class UserCog(commands.Cog, name="Commands"):
    '''
    Commands available to all players

    These commands involve querying and manipulating the
    role queues.
    '''
    def __init__(self, bot):
        self.bot = bot
        ghostcourt.debug("User cog started")

    @commands.command(name='cq')
    async def list_queue(self, ctx, *args):
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
        ghostcourt.debug('listing queues with args:')
        ghostcourt.debug_obj(args)

        msg_response = list()

        try:
            if len(args) == 0:
                ghostcourt.debug("zero args -- listing for user {0}", ctx.author)
                msg_response.append(ghostcourt.list_user_queue(ctx.author))

            else:
                ghostcourt.debug("{0} args", len(args))
                for arg in args:
                    msg_response.append(ghostcourt.list_role_queue(arg))
                # iterate
                pass
        except Exception as e:
            ghostcourt.debug("Whoops...")
            ghostcourt.debug_obj(e)

        for msg in msg_response:
            ghostcourt.debug("sending message...")
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
        ghostcourt.debug('Got request to enqueue for {0}', roles)
        user = ctx.author
        ghostcourt.enqueue(user, roles)
        await ctx.send(ghostcourt.list_user_queue(user))

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

            !dq plaintiff reporter

        You may also use aggregate role names here.
        '''
        ghostcourt.debug('Got request to dequeue from {0}', roles)
        user = ctx.author
        ghostcourt.dequeue(user, roles)
        await ctx.send(ghostcourt.list_user_queue(user))
