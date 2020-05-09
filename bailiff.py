# Bailiff cog
from discord.ext import commands

class BailiffCog(commands.Cog, name="Bailiff commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role('Bailiff')
    @commands.command(name='qser', help='Add a user to queues')
    async def enqueue_user(ctx, user, *roles):
        pass

    
    @commands.has_role('Bailiff')
    @commands.command(name='dqser', help='Remove a user from queues')
    async def dequeue_user(ctx, user, *roles):
        pass

