# Class representing the case queue
from ghostcourt import debug, debug_obj
from case import Case
from rolequeue import RoleQueue
import yaml
import math, random

class CaseQueue(object):
    '''
    Singleton class representing the queue of cases
    '''
    __instance = None
    def __new__(cls, *args, **kwargs):
        if CaseQueue.__instance is None:
            CaseQueue.__instance = object.__new__(cls)
        return CaseQueue.__instance

    # case definitions available
    hopper = []
    # queue of upcoming cases
    docket = []
    # next case to become active
    queued = None
    # currently active case
    current = None
    # history of cases seen
    history = []

    def load(self, filename):
        '''
        Load case definitions from file
        '''
        try:
            stream = open(filename, 'r')
        except Exception as e:
            print("Error encountered parsing case file: {0}".format(filename))
            raise e

        with stream as casefile:
            for entry in yaml.safe_load_all(casefile):
                case = Case(entry)
                if case:
                    CaseQueue.hopper.append(case)

    def status(self):
        yield "Cases in the hopper: {0}".format(len(CaseQueue.hopper))
        for case in CaseQueue.hopper:
            yield "> {0}: {1}".format(case.case, case.title)
        yield "Cases in the docket: {0}".format(len(CaseQueue.docket))
        for case in CaseQueue.docket:
            yield "> {0}: {1}".format(case.case, case.title)
        yield "Current case:"
        if CaseQueue.current:
            yield "> {0}: {1}".format(CaseQueue.current.case, CaseQueue.current.title)
        else:
            yield "None"
        yield "Cases completed this session: {0}".format(len(CaseQueue.history))
        for case in CaseQueue.history:
            yield "> {0}: {1}".format(case.case, case.title)

    def add(self, case):
        '''
        Given a case number, add that case to the case queue
        '''
        pass

    def next(self):
        '''
        Close out the current case and start a new one. 

        This involves:
        - Remove litigant roles
        - If an officer is to step down, remove their role
        - Assign new litigant roles
        - Fill vacant officer roles
        - Announce the new case
        '''
        debug("Making sure we have a full lineup for the next case")
        rq = RoleQueue()
        lineup = rq.lineup()
        for role, member in lineup.items():
            if member is None:
                raise Exception("Not enough players to fill all roles")

        debug("Ending current case")
        if not self.current is None:
            # remove roles from current case
            # move current case into history
            self.history.append(self.current)
            self.current = None

        debug("Loading new case")
        if (len(self.docket) == 0):
            raise Exception("No more cases on the docket")

        new_case = self.docket.pop(0)
        new_case.plaintiffUser = lineup.get("plaintiff")
        new_case.defendantUser = lineup.get("defendant")
        new_case.judgeUser = lineup.get("judge")

        debug("Assigning new roles and remove from queues")
        # TODO assign new roles
        rq.remove(new_case.plaintiffUser, list())
        rq.remove(new_case.defendantUser, list())
        rq.remove(new_case.judgeUser, list())

        debug("Setting new case as current")
        self.current = new_case
        pass

    def list(self):
        pass

    def choose(self, range=10):
        '''
        Choose and enqueue a single case from the next few in the
        hopper
        '''
        debug("Adding a random case to the docket")
        spread = min(range, len(CaseQueue.hopper))
        index = math.floor(random.random() * spread)
        case = CaseQueue.hopper.pop(index)
        CaseQueue.docket.append(case)
        pass
