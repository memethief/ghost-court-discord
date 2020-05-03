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
