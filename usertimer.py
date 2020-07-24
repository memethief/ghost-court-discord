# Class representing a timer for a given user
import asyncio, time, threading
from ghostcourt import debug, debug_obj, message_roles

class UserTimer:
    # identifying label for this timer
    label = "anonymous"
    # timer duration, in seconds
    duration = 5
    # messages to send at start and upon completion
    startMessage = "anonymous timer started"
    endMessage = "anonymous timer finished"
    # recipients of message. Each of these is a role.
    recipientRoles = {"Judge", "Clerk", "Plaintiff"}
    # timer state
    running = False

    timers = dict()

    @classmethod
    def get(cls, label):
        if label in UserTimer.timers:
            return UserTimer.timers[label]
        else:
            return None

    @classmethod
    def start(cls):
        if not cls.label in UserTimer.timers:
            UserTimer.timers[cls.label] = cls()

        timer = UserTimer.timers[cls.label]

        if not timer:
            debug("Something went wrong starting a {0} timer", cls.label)
            raise "Something went wrong starting a {0} timer".format(cls.label)

        timer.thread = threading.Timer(cls.duration, timer.complete)
        timer.thread.start()

        debug(cls.startMessage)

    @classmethod
    def cancel(cls):
        if not cls.label in UserTimer.timers:
            debug("Tried to stop missing {0} timer", cls.label)
            return

        debug("Stopping {0} timer...", cls.label)
        UserTimer.timers[cls.label].cancel()
        debug("Stopped {0} timer.", cls.label)

    def complete(self):
        # send a message
        debug(self.endMessage)
        pass

class PlaintiffTimer(UserTimer):
    label = "Plaintiff"
    duration = 3 # 60
    startMessage = "The plaintiff has one minute to present their case."
    endMessage = "The plaintiff's time to present their case is up."
    recipientRoles = ["Judge", "Clerk", "Plaintiff"]

async def main():
    debug("Starting main at {0}", time.strftime('%X'))
    # Schedule a timer

    aTimer = UserTimer(4,"Done!", ["Clerk"])
    bTimer = UserTimer(2,"Done!", ["Clerk"])

    debug("Prepping direct run at {0}", time.strftime('%X'))
    direct = asyncio.create_task(bTimer.run('b'))
    await direct

    debug("Starting asyncio and direct runs at {0}", time.strftime('%X'))

    await asyncio.create_task(aTimer.run('a'))
    await direct

    #debug("Completed main at {0}", time.strftime('%X'))

#asyncio.run(main())
#debug("Completed script at {0}", time.strftime('%X'))
