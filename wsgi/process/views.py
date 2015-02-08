from advanced.render import renderJSON

def startProcess(request,process):
    """
    Starts a :class:`.Process` identified from *process*
    """
    startProcess(process)
    return renderJSON(request, None)

def setBreakPoint(request,process,stage,step):
    """
    Set breakpoint for the :class:`.Process` identified from *process*.
    *stage* sets as 'break_stage' of :class:`.Progress`.
    *step* set as 'break_point' of :class:`.Progress`.
    """
    pass

def getAllProcesses(request):
    """
    Returns all :class:`.Process` item information.
    """
    pass

def getProcessProgress(request,process):
    """
    Get progress information related to :class:`.Process` identified by *process*
    """
    return renderJSON(request, getProcessProgress(process))
