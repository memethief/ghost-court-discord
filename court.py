# Court class
# TODO combine these two classes into one
'''
Class defining the different states of the game as a whole.
'''
from enum import Enum, auto

class CourtState(Enum):
	# Waiting: we don't know yet if we're ready to load a case
	WAITING = auto()
	# Ready: We have all we need to load a case
	#READY = auto()
	# Active: A case has been loaded and is ready to be introduced
	ACTIVE = auto()
	# Plaintiff: The plaintiff's turn to speak has begun
	PLAINTIFF = auto()
	# Defendant: The defendant's turn to speak has begun
	DEFENDANT = auto()
	# Judge: The judge's deliberation period has begun
	JUDGE = auto()
	# Closed: The case has been closed
	CLOSED = auto()

	#def initialize(self):

class Court:
    '''
    Singleton class representing the game as a whole
    '''
    #__instance = None
    state = CourtState.WAITING
    #def __new__(cls):
    #    if Court.__instance is None:
    #        Court.__instance = object.__new__(cls)
    #        #Court.__instance.state = CourtState.WAITING
    #    return Court.__instance

    stateMachine = {
    	CourtState.WAITING: CourtState.ACTIVE,
    	#CourtState.READY: CourtState.ACTIVE,
    	CourtState.ACTIVE: CourtState.PLAINTIFF,
    	CourtState.PLAINTIFF: CourtState.DEFENDANT,
    	CourtState.DEFENDANT: CourtState.JUDGE,
    	CourtState.JUDGE: CourtState.CLOSED,
    	CourtState.CLOSED: CourtState.WAITING
    }

    @classmethod
    def next(cls):
    	cls.state = cls.stateMachine.get(cls.state)
    	pass
