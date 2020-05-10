# bot.py
import os
import random
import discord

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
        
''' Run bot, run! '''

import bailiff
import clerk
import user

bot.add_cog(bailiff.BailiffCog(bot))
bot.add_cog(clerk.ClerkCog(bot))
bot.add_cog(user.UserCog(bot))

bot.run(TOKEN)
