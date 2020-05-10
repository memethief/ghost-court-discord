from pprint import pprint

# Other actions

def list_user_queue(user):
    '''
    Given a user object, if the user corresponds 
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

def list_role_queue(role):
    debug("Listing queue for role: {0}".format(role))
    
    listing = []
    q = qs.get(role)
    if q == None:
        raise InvalidArgument("Unknown role {0}".format(role))

    index = 0
    for user in q:
        listing.append("{0}: {1}".format(index, user))
        index += 1

    if index == 0:
        listing.append("{0} queue is empty".format(role))
    else:
        listing.insert(0, "{0} queue:".format(role))

    response = '\n'.join(listing)
    debug('Message to send:')
    debug(response)
    return response

def enqueue(user, roles):
        '''
        Add a user to a queue or queues
        
        One may also use aggregate role names here.

        Note that this command does not affect user's current
        place in any queues they have already joined.
        '''
        debug('Going to enqueue {1} into {0}', roles, user)

        if len(roles) == 0:
            debug("Let's enqueue everywhere!")
            roles = ['all']

        for role in translate_roles(roles):
            debug("Processing role {0}", role)
            q = qs.get(role)

            if q == None:
                debug('Bad role {0} requested', role)
                continue

            if user in q:
                debug('User {0} already in {1} queue', user, role)
                continue

            debug("Appending user to {0} queue", role)
            q.append(user)

        debug('Finished adding to queues')

def dequeue(user, roles):
    '''
    Remove a user from a queue or queues
    
    One may also use aggregate role names here.
    '''
    debug('Going to dequeue {1} from {0}', roles, user)

    if len(roles) == 0:
        debug("Let's dequeue everywhere!")
        roles = ['all']

    for role in translate_roles(roles):
        debug("Processing role {0}", role)
        q = qs.get(role)
        
        if q == None:
            debug('Bad role {0} requested', role)
            continue

        if not user in q:
            debug('User {0} not in {1} queue', user, role)
            continue
        
        debug("Removing user from queue")
        q.remove(user)

    debug('Finished removing from queues')

def empty_queue(user, roles):
    '''
    Given a list of roles, empty their queues
    '''
    pass

def add_case(user, cases):
    '''
    Given a case number, add that case to the case queue
    '''
    pass

def next_case(user, args):
    '''
    Close out the current case and start a new one. This involves:
    - Remove litigant roles
    - If an officer is to step down, remove their role
    - Assign new litigant roles
    - Fill vacant officer roles
    - Announce the new case
    '''
    debug("Ending current case")
    debug("Loading new case")
    debug("Assigning new roles")
    pass

def terminate_bot(*args):
    debug('about to terminate the bot...')
    exit()

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

cases = []
current_case = {
    'docketNumber': None,
    'plaintiffName': None,
    'plaintiffUser': None,
    'defendantName': None,
    'defendantUser': None,
    'judgeUser': None,
}

# Debug

def debug(message, *args):
    print(message.format(*args), flush=True)

def debug_obj(obj):
    print(obj, flush=True)
    pprint(obj)