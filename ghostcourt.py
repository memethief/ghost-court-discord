from pprint import pprint
import discord

# Other actions

def terminate_bot(*args):
    debug('about to terminate the bot...')
    exit()

# Debug

def debug(message, *args):
    print(message.format(*args), flush=True)

def debug_obj(obj):
    pprint(obj)

def mention2member(ctx, mentionString):
	# Given a mention string, return the corresponding user
	debug("Trying to turn {0} into a member", mentionString)
	debug("querying {0} for members", ctx.guild)
	for m in ctx.guild.members:
		debug("{0} is {1}/{2}", m.name, m.id, m.mention)
	import re
	member_id_string = re.search("\d+", mentionString).group()
	if member_id_string is None:
		debug("no id number found in string")
		return mentionString
	debug("Parsed out id: {0}", member_id_string)
	member_id_int = int(member_id_string)
	found = discord.utils.get(ctx.guild.members, id=member_id_int)
	if found is None:
		debug("no member found with the given id number")
		return mentionString
	debug("Success!")
	debug_obj(found)
	return found

def resolve_member(ctx, member):
	found = member
	debug("trying to resolve {0}", found)
	if isinstance(found, str):
		found = mention2member(ctx, found)
	if isinstance(found, discord.Member):
		return found
	raise Exception("Could not resolve member object from [{0}]".format(member))

def get_role_members(ctx, roles):
	# Given a list of roles, return all users with any of those roles
	debug("Looking for members of {0} with roles:\n{1}", ctx.guild, roles)
	for foundrole in ctx.guild.roles:
		debug("Found role:  {0}", foundrole.name)
	
	found = set()

	for role in filter(lambda r: r.name in roles, ctx.guild.roles):
		found.update(role.members)

	return found

async def message_roles(ctx, message, roles):
    '''
    Given a message and some roles, send the message to any user with one
    of the given roles.
    '''
    debug("Sending message to {0}", roles)
    members = get_role_members(ctx, roles)
    debug("Resolved members: {0}", members)
    for member in members:
    	debug("Sending to {0}", member.nick)
    	await member.send(message)
