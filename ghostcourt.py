from pprint import pprint

# Other actions

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

# Queues 

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
