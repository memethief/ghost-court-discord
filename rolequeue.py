# Class representing the role queue

class RoleQueue():
	'''
	Class representing the collection of role queues
	'''

	def list_user(self, user):
	    '''
	    Given a user object, list all queues containing the user
	    along with their position in each
	    '''
	    debug("Listing queues for user: {0}", user)
	    
	    listing = []
	    for role, q in qs.items():
	        if user in q:
	            listing.append('- {0}: at most {1} people ahead of you'.format(
	                role.capitalize(), q.index(user)
	                ))

	    if len(listing) == 0:
	        listing.append('**{0} is in no queues**'.format(user.mention))
	    else:
	        listing.insert(0,'**{0} is in the following queues:**'.format(user.mention))

	    response = '\n'.join(listing)
	    debug('Message to send:')
	    debug(response)
	    return response

	'''
	Return a list of strings, each one being a representation of a queue
	'''
	def list(self, roles):
	    debug("Listing queue for roles: {0}".format(roles))

	    response = []
	    
	    for role in translate_roles(roles):
	        q = qs.get(role)
	        if q == None:
	            raise ValueError("Unknown role {0}".format(role))

	        listing = []
	        if len(q) == 0:
	            listing.append("{0} queue is empty".format(role))
	        else:
	            listing.append("{0} queue:".format(role))

	            index = 0
	            for user in q:
	                listing.append("{0}: {1}".format(index, user))
	                index += 1

	        message = '\n'.join(listing)
	        debug('Message to send:')
	        debug(message)
	        response.append(message)

	    return response

	def add(self, user, roles):
	    '''
	    Add a user to a queue or queues
	    
	    One may also use aggregate role names here.

	    Note that this command does not affect user's current
	    place in any queues they have already joined.
	    '''
	    debug('Going to enqueue {1} into {0}', roles, user)
	    response = dict()

	    if len(roles) == 0:
	        debug("Let's enqueue everywhere!")
	        roles = ['all']

	    for role in translate_roles(roles):
	        debug("Processing role {0}", role)
	        q = qs.get(role)

	        if q == None:
	            debug('Bad role {0} requested', role)
	            response[role] = "No such role"
	            continue

	        if user in q:
	            debug('User {0} already in {1} queue', user, role)
	            response[role] = "Already in queue"
	            continue

	        debug("Appending user to {0} queue", role)
	        q.append(user)
	        response[role] = "OK"

	    debug('Finished adding to queues')
	    return response

	def remove(self, user, roles):
	    '''
	    Remove a user from a queue or queues
	    
	    One may also use aggregate role names here.
	    '''
	    debug('Going to dequeue {1} from {0}', roles, user)
	    response = dict()

	    if len(roles) == 0:
	        debug("Let's dequeue everywhere!")
	        roles = ['all']

	    for role in translate_roles(roles):
	        debug("Processing role {0}", role)
	        q = qs.get(role)
	        
	        if q == None:
	            debug('Bad role {0} requested', role)
	            response[role] = "No such role"
	            continue

	        if not user in q:
	            debug('User {0} not in {1} queue', user, role)
	            response[role] = "Not in queue"
	            continue
	        
	        debug("Removing user from queue")
	        q.remove(user)
	        response[role] = "OK"

	    debug('Finished removing from queues')
	    return response

	def clear(roles):
	    '''
	    Given a list of roles, empty their queues
	    '''
	    debug("Going to empty queues: {0}", roles)
	    response = dict()

	    if len(roles) == 0:
	        debug("Empty argument list given")
	        raise ValueError("Must specify queue or queues to empty")

	    for role in translate_roles(roles):
	        debug("Processing role {0}", role)
	        q = qs.get(role)
	        
	        if q == None:
	            debug('Bad role {0} requested', role)
	            response[role] = "No such role"
	            continue

	        debug("Emptying queue")
	        q.clear()
	        response[role] = "OK"

	    debug('Finished emptying queues')
	    return response
