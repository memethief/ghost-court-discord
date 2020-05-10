# Bailiff cog
from discord.ext import commands
import ghostcourt

class BailiffCog(commands.Cog, name="Bailiff commands"):
    def __init__(self, bot):
        self.bot = bot
        ghostcourt.debug("Clerk cog started")

    @commands.has_role('Bailiff')
    @commands.command(name='qser', help='Add a user to queues')
    async def enqueue_user(self, ctx, user, *roles):
        '''
        Add a user to a queue or queues
        
        By itself this command will add the given user to all
        role queues. You can limit this to specific queues by 
        following the command with one or more role names. For 
        example, to add the user only to the plaintiff and clerk
        queues, you may type:

            !quser <username> plaintiff clerk

        You may also use aggregate role names here.

        Note that this command does not affect the user's current
        place in any queues they have already joined. If you
        want to move them to the back of a queue you must use 
        !dqser, followed by !qser.
        '''
        ghostcourt.debug('Got request to enqueue {1} for {0}', roles, user)
        response = ["Adding {0} to roles:".format(user)]
        for role, status in ghostcourt.enqueue(user, roles).items():
            response.append(" {0}: {1}".format(role, status))
        response.append("Finished enqueuing {user}")
        await ctx.send("\n".join(response))

    
    @commands.has_role('Bailiff')
    @commands.command(name='dqser', help='Remove a user from queues')
    async def dequeue_user(self, ctx, user, *roles):
        '''
        Remove a user from a queue or queues
        
        By itself this command will remove the specified user from 
        all role queues. You can limit this to specific queues by
        following the command with one or more role names. For 
        example, if you want to remove the user from the defendant 
        and reporter queues but keep their place in all other queues, 
        you may type:

            !dqser defendant reporter

        You may also use aggregate role names here.
        '''
        ghostcourt.debug('Got request to dequeue {1} from {0}', roles, user)
        response = ["Removing {0} from roles:".format(user)]
        for role, status in ghostcourt.dequeue(user, roles).items():
            response.append(" {0}: {1}".format(role, status))
        response.append("Finished dequeuing {user}")
        await ctx.send("\n".join(response))

