from process.models import getProcess
from threading import Thread


def _runProcess(text):
    """
    Executes series of functions mentioned by :class:`.Stage`s of the :class:`.Process`
    identified by *text*
    """
    process = getProcess(text)
    #TODO check same process already running
    #start thread;
    progress = process.getProgress()
    stages = process.getStages()
    for i in range(progress.stage.index, len(stages)):
        if i==-1:
            continue
        elif i <= progress.break_stage.index:
            progress.setStage(stages[i])
        else:
            break
        if not progress.progress:
            progress.progress = 0
        if 0 < progress.progress:
            progress.decrement()
        stages[i].execute()
        progress.clear()
    progress.reset()


def startProcess(text):
    """
    Starts thread to execute series of functions mentioned in each :class:`.Stage` belongs to the :class:`.Process`
    identified by given *text*. State of the executing :class:`.Stage` and progress information are recorded in
    :class:`.Progress`.
    """
    t =Thread(name=text, target=_runProcess, args = (text,))
    t.daemon = True
    t.start()