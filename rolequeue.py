# Class representing the role queue
from ghostcourt import debug, debug_obj

class RoleQueue(object):
    '''
    Singleton class representing the collection of role queues
    '''
    __instance = None
    def __new__(cls):
        if RoleQueue.__instance is None:
            RoleQueue.__instance = object.__new__(cls)
            RoleQueue.__instance.qs = {
                'plaintiff': [],
                'defendant': [],
                'judge': [],
                'reporter': [],
                #'clerk': [],
                #'bailiff': []
            }
        return RoleQueue.__instance

    def list_user(self, user):
        '''
        Given a user object, list all queues containing the user
        along with their position in each
        '''
        debug("Listing queues for user: {0}", user)
        
        listing = []
        for role, q in self.qs.items():
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

    def list(self, roles):
        '''
        Return a list of strings, each one being a representation of a queue
        '''
        debug("Listing queue for roles: {0}".format(roles))

        response = []
        
        for role in self.translate_roles(roles):
            q = self.qs.get(role)
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

        for role in self.translate_roles(roles):
            debug("Processing role {0}", role)
            q = self.qs.get(role)

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

        for role in self.translate_roles(roles):
            debug("Processing role {0}", role)
            q = self.qs.get(role)
            
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

    def clear(self, roles):
        '''
        Given a list of roles, empty their queues
        '''
        debug("Going to empty queues: {0}", roles)
        response = dict()

        if len(roles) == 0:
            debug("Empty argument list given")
            raise ValueError("Must specify queue or queues to empty")

        for role in self.translate_roles(roles):
            debug("Processing role {0}", role)
            q = self.qs.get(role)
            
            if q == None:
                debug('Bad role {0} requested', role)
                response[role] = "No such role"
                continue

            debug("Emptying queue")
            q.clear()
            response[role] = "OK"

        debug('Finished emptying queues')
        return response

    def translate_roles(self, roles):
        '''
        Look for special role names in the list of roles and return a modified
        list with those names expanded
        '''
        debug("translating roles {0}...", roles)
        new_roles = set()
        for role in roles:
            role = role.lower()
            if role == 'all':
                new_roles = self.qs.keys()
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

    def lineup(self):
        '''
        Return a dictionary of the next users and their roles

        Note that this does not actually modify any queues, it just 
        tells us what roles each person would have if assigned right 
        now.
        '''
        debug("figuring out who gets which role")
        # Create a copy of our dictionary of role queues
        qsc = dict()
        for role, q in self.qs.items():
            qsc[role] = q.copy()

        # First we want to assign the role with the fewest queued 
        # users. This hopefully helps avoid running out of options 
        # for a given role
        debug("sorting queues by length")
        sorted_roles = sorted(qsc.keys(), key=lambda rolename: len(qsc[rolename]))
        debug("sorted queues:")
        for role in sorted_roles:
            names = list()
            for member in qsc[role]:
                names.append(member)
            debug("{0}: {1}", role, names)

        debug("building dictionary of roles")
        role_dict = dict()

        # Start with the shortest role queue
        for role in sorted_roles:
            if len(qsc[role]) == 0:
                # if the queue is empty we can't assign the role
                debug("Nobody in line for {0}", role)
                role_dict[role] = None
                continue

            # get the chosen member
            chosen = qsc.get(role).pop()
            # and remove them from all other queues
            for key, alist in qsc.items():
                if chosen in alist:
                    alist.remove(chosen)

            debug("{0} gets the role of {1}", chosen, role)
            role_dict[role] = chosen

        # done
        return role_dict
