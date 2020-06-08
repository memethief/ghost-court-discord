# Bailiff cog
from discord.ext import commands
from ghostcourt import debug, debug_obj, resolve_member
from rolequeue import RoleQueue

class BailiffCog(commands.Cog, name="Bailiff commands"):
    def __init__(self, bot):
        self.bot = bot
        self.rq = RoleQueue()
        debug("Bailiff cog started")

    @commands.has_role('Bailiff')
    @commands.command(name='qser')
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
        debug('resolving member object...')
        member = resolve_member(ctx, user)
        debug('Got request to enqueue {1} for {0}', roles, member.name)
        response = ["Adding {0} to roles:".format(member.mention)]
        for role, status in self.rq.add(member, roles).items():
            response.append(" {0}: {1}".format(role, status))
        response.append("Finished enqueuing {0}".format(member.mention))
        await ctx.send("\n".join(response))
    
    @commands.has_role('Bailiff')
    @commands.command(name='dqser')
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
        debug('resolving member object...')
        member = resolve_member(ctx, user)
        debug('Got request to dequeue {1} from {0}', roles, member.name)
        response = ["Removing {0} from roles:".format(member.mention)]
        for role, status in self.rq.remove(member, roles).items():
            response.append(" {0}: {1}".format(role, status))
        response.append("Finished dequeuing {0}".format(member.mention))
        await ctx.send("\n".join(response))
    
    @commands.has_role('Bailiff')
    @commands.command(name='mtq')
    async def empty_queue(self, ctx, *roles):
        '''
        Empty out an entire queue or queues

        This command will clear all users from the named queue or
        queues. For example, to empty the Bailiff queue, type:

            !mtq bailiff


        A role or roles must be specified; calling this command 
        without arguments is an error. You can empty all queues 
        with the command:

            !mtq all
        '''
        debug('Got request to empty {0}', roles)
        response = ["Emptying queues:"]
        for role, status in self.rq.clear(roles).items():
            response.append(" {0}: {1}".format(role, status))
        response.append("Finished empying queues")
        await ctx.send("\n".join(response))

