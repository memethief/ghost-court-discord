from pprint import pprint

# Other actions

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
