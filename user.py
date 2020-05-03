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

    @commands.command(name='cq')
    async def list_queue(ctx, *args):
        '''
        List contents of queues

        By default, list all active queues you have joined.
        This will include information about how many people
        are ahead of you.
        '''
        debug('listing queues with args:')
        debug_obj(args)

        msg_response = list()

        try:
            if len(args) == 0:
                debug("zero args -- listing for user {0}", ctx.author)
                msg_response.append(list_user_queue(ctx.author))

            else:
                debug("{0} args", len(args))
                # iterate
                pass
        except e:
            debug("Whoops...")
            debug_obj(e)

        for msg in msg_response:
            debug("sending message...")
            await ctx.send(msg)

    @commands.command(name='q')
    async def enqueue(ctx, *roles):
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

        if len(roles) == 0:
            debug("Let's enqueue everywhere!")
            roles = ['all']

        for role in translate_roles(roles):
            debug("Processing role {0}", role)
            q = qs.get(role)

            if q == None:
                debug('Bad role {0} requested', role)
                continue

            if user in q:
                debug('User {0} already in {1} queue', user, role)
                continue

            debug("Appending user to {0} queue", role)
            q.append(user)

        debug('Finished adding to queues')
        await ctx.send(list_user_queue(user))

    @commands.command(name='dq')
    async def dequeue(ctx, *roles):
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
        debug('Got request to dequeue from {0}', roles)
        user = ctx.author

        if len(roles) == 0:
            debug("Let's dequeue everywhere!")
            roles = ['all']

        for role in translate_roles(roles):
            debug("Processing role {0}", role)
            q = qs.get(role)
            
            if q == None:
                debug('Bad role {0} requested', role)
                continue

            if not user in q:
                debug('User {0} not in {1} queue', user, role)
                continue
            
            debug("Removing user from queue")
            q.remove(user)

        debug('Finished removing from queues')  
        await ctx.send(list_user_queue(user))
