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

# Other actions

def list_user_queue(user):
    '''
    Given a user object, if the user corresponds 
    '''
    debug("Listing queues for user: {0}", user)
    
    listing = []
    for role, q in qs.items():
        if user in q:
            listing.append('- {0}: at most {1} people ahead of you'.format(role.capitalize(), q.index(user)))

    if len(listing) == 0:
        listing.append('**{0} is in no queues**'.format(user.mention))
    else:
        listing.insert(0,'**{0} is in the following queues:**'.format(user.mention))

    response = '\n'.join(listing)
    debug('Message to send:')
    debug(response)
    return response

''' Helper function '''

def translate_roles(roles):
    '''
    Look for special role names in the list of roles and return a modified
    list with those names expanded
    '''
    debug("translating roles {0}...", roles)
    new_roles = set()
    for role in roles:
        role = role.lower()
        if role == 'all':
            new_roles = qs.keys()
            break
        elif role == 'litigant':
            new_roles.add('plaintiff')
            new_roles.add('defendant')
        elif role == 'officer':
            new_roles.add('judge')
            new_roles.add('clerk')
            new_roles.add('reporter')
        else:
            new_roles.add(role)

    debug("...translated to {0}", new_roles)
    return new_roles

# Queues 
qs = {
    'plaintiff': [],
    'defendant': [],
    'judge': [],
    'reporter': [],
    'clerk': [],
    'bailiff': []
}

# Debug

def debug(message, *args):
    print(message.format(*args), flush=True)

def debug_obj(obj):
    print(obj, flush=True)

''' Run bot, run! '''

import user

bot.add_cog(user.UserCog(bot))
bot.run(TOKEN)
