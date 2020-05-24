# Class representing a single case
from ghostcourt import debug, debug_obj

class Case():
    '''
    Class representing a single case
    '''
    docketNumber = None
    plaintiffName = None
    plaintiffUser = None
    defendantName = None
    defendantUser = None
    judgeUser = None

    def __new__(cls, content, *args, **kwargs):
        if not content:
            return None

        instance = object.__new__(cls)
        instance.parse(content)
        if hasattr(instance, "case"):
            return instance
        else:
            return None

    def parse(self, content):
        self.__dict__.update(content)

    def __getattr__(self, name):
        if name == "title":
            return "{0} v {1}".format(self.plaintiff["name"], self.defendant["name"])

        # else
        return object.__getattr__(self, name)
