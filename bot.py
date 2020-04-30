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
        await ctx.send('Unknown error: {0}', error)
        
# Commands

@bot.command(name='poc', hidden=True)
async def poc(ctx, *args):
    debug("Proof of concept. args:")
    debug_obj(args)
    debug("Author:")
    pprint(ctx.author)

    response = 'Hello {0} how are you?'.format(ctx.author.mention)
    
    await ctx.send(response)

# Debug

def debug(message, *args):
    print(message.format(*args), flush=True)

def debug_obj(obj):
    print(obj, flush=True)

''' Run bot, run! '''

bot.run(TOKEN)
