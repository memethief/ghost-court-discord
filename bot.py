# bot.py
import os
import random
import discord
import ghostcourt

from discord.ext import commands
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))

bot = commands.Bot(command_prefix='!')

# Events

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
        await ctx.send('Unknown error: {0}'.format(error))
        
# Commands

@bot.command(name='poc', hidden=True)
async def poc(ctx, *args):
    ghostcourt.debug("Proof of concept. args:")
    ghostcourt.debug_obj(args)
    ghostcourt.debug("Author:")
    pprint(ctx.author)

    response = 'Hello {0} how are you?'.format(ctx.author.mention)
    
    await ctx.send(response)

''' Run bot, run! '''

import bailiff
import clerk
import user

bot.add_cog(bailiff.BailiffCog(bot))
bot.add_cog(clerk.ClerkCog(bot))
bot.add_cog(user.UserCog(bot))

bot.run(TOKEN)
