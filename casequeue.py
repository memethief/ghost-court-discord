# Class representing the case queue
from ghostcourt import debug, debug_obj

class CaseQueue(object):
    '''
    Singleton class representing the queue of cases
    '''
    __instance = None
    def __new__(cls):
        if CaseQueue.__instance is None:
            CaseQueue.__instance = object.__new__(cls)
            CaseQueue.__instance.q = []
        return CaseQueue.__instance

    def add(self, case):
        '''
        Given a case number, add that case to the case queue
        '''
        pass

    def next(self):
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
