import uuid

class ExecResult:
    caseID = ""
    groupName = ""
    caseType = ""
    results=dict()

    @staticmethod
    def __log(message, value):
        print("{0}: '{1}'".format(message, value))
        return value

    def __init__(self, caseID, caseType, groupName = ""):
       self.caseID = __log("Create object with case ID", caseID)
       self.caseType = __log("and type", caseType)
       self.groupName = __log("in group", groupName)

    def addResult(self, elapsed, status):
        s = __log("Add result of attend with status", status)
        e = __log("and elapsed time", elapsed.split("s")[0])
        g = __log("to GUID", uuid.uuid4())
        self.results[g] = [e, s]

#    def getElapsed