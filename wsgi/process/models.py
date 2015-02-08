from django.db import models
from advanced.autoimport import importFunction



class Process(models.Model):
    """
    A Process responsible for executing series of functions kept on each :class:`Stage`. Each :class:`Stage`'s function is executed
    using :func:`Stage.execute`. Information related to execution is preserved in :class:`Progress`. Breakpoints can be setup by 
    modifying :class:`Progress`. Each Process have it's own :class:`Progress` instance.
    
    * *name*
    * *name*
    * *description*
    * *last_run*
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, unique=True, blank=True)
    description = models.TextField(null=True, blank=True)
    last_run = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'log_process'

    def __unicode__(self):
        return self.name
    
    def getProgress(self):
        """
        Returns the :class:`Progress` object of the :class:`Process`.
        """
        return Progress.objects.get(process=self)
    
    def getStages(self):
        """
        Returns all :class:`Stage` items belongs to the :class:`Process` ordered by
        :class:`Stage` index.
        """
        return Stage.objects.filter(process=self).order_by('index')
        

class Stage(models.Model):
    """
    Holds information of all stages belongs to each :class:`Process`.
    
    * *process*
    * *index* - Index of the stage of the process.
    * *stage_message*
    * *stage_function_name* - Name of the function that wii be executed in the current stage.
    * *stage_function_module* - Module name of the stage function belongs.
    * *stage_function_file* - File name of the stage function.
    
    
    """
    id = models.AutoField(primary_key=True)
    process = models.ForeignKey(Process)
    index = models.IntegerField(null=True, blank=True)
    stage_message = models.TextField(unique=True, blank=True)
    stage_function_module = models.CharField(max_length=45, blank=True)
    stage_function_file = models.CharField(max_length=45, blank=True)
    stage_function_name = models.CharField(max_length=45, blank=True)

    class Meta:
        db_table = 'log_stage'

    def __unicode__(self):
        return str(self.index)
    
    def execute(self):
        """
        Executes the function identified using 'stage_function_name' value. until it completes or reach the
        breakpoint
        """
        bri = self.process.getProgress().break_stage.index
        if bri != -1 and self.index <= bri:
            function = importFunction(self.stage_function_module, self.stage_function_file, self.stage_function_name)
            function()

class Progress(models.Model):
    """
    Progress keeps information about currently executing function, progress information and break-point information.
    
    * *process*
    * *stage*
    * *progress* -current progress of the stage
    * *complete*
        Sets number of steps in the stage. this will set automatically if the stage method implemented
        with :func:`setProgressBoundary`.
    * *break_stage* 
        If the stage is not empty the process will execute that stage as the last stage 
        before terminate.
    * *break_point*
        This can be set manually along with break_stage. The :class:`Stage` will terminated after executing
        step mentioned in the break_point.
    """
    id = models.AutoField(primary_key=True)
    process = models.ForeignKey(Process)
    stage = models.ForeignKey(Stage, related_name="stage")
    progress = models.IntegerField(null=True, blank=True)
    complete = models.IntegerField(null=True, blank=True)
    break_stage = models.ForeignKey(Stage, related_name="stage_break_point")
    break_point = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'log_progress'

    def __unicode__(self):
        return str(self.id)
    
    def clear(self):
        """
        Clears the progress of the :class:`Progress` and reset *complete* value to 1.
        """
        if self.break_stage != self.stage:
            self.progress = 0
            self.complete = 1
            self.save()
        
    def decrement(self):
        self.progress -= 1
        self.save()
        
    def setStage(self,stage):
        """
        Sets the *stage* of the :class:`Progress`.
        """
        self.stage = stage
        self.save()
        
    def reset(self):
        """
        Set stage of this :class:`Progress` to the initial :class:`Stage` and
        clears the progress of the :class:`Progress` and reset *complete* value to 1 
        as well.
        """
        if self.break_stage.index == -1:
            self.progress = 0
            self.complete = 1
            Q1 = Stage.objects.get(process=self.process, index=0)
            self.stage = Q1
            self.save()

#deprecated        
def incrementProgress(text):
    """
    This function increments the value of completed steps in the current :class:`Stage` 
    of :class:`Process` identified by *text*. This function should be implemented in steps 
    that takes considerably long time to complete. That will help to track down the progress 
    of the current :class:`Stage`. This function will raise an exception if incrementing value 
    passed the breakpoint defined within :class:`Progress`. This method should not use twice 
    within single step to avoid incrementing step count twice. However it will not affects
    execution of the function. But it will results erroneous step count and affects the breakpoint
    
    :func:`setProgressBoundary` and :func:`getCurrentProgress` should also be implemented along 
    with this function.
    """
    Q1 = Process.objects.filter(name=text)
    if Q1:
        progress = Q1[0].getProgress()
        if not progress.progress:
            progress.progress = 0
        if progress.stage and progress.break_stage and progress.stage == progress.break_stage and progress.break_point <= progress.progress:
            raise Exception('Reached break-point.')
        progress.progress += 1
        progress.save()

def breakNow(text):
    """
    This method is deprecated. use :func:`incrementProgress` instead.
    """
    Q1 = Process.objects.filter(name=text)
    if Q1:
        progress = Q1[0].getProgress()
        if not progress.progress:
            progress.progress = 0
        if progress.stage and progress.break_stage and progress.stage == progress.break_stage and progress.break_point <= progress.progress:
            return True
        progress.progress += 1
        progress.save()
        return False

def setProgressBoundary(text,num):
    """
    Set upper boundary as *num* of the current :class:`Stage` of the :class:`Process` identified by *text*.
    """
    Q1 = Process.objects.filter(name=text)
    if Q1:
        progress = Q1[0].getProgress()
        progress.complete = num
        progress.save()
    
def getCurrentProgress(text):
    """
    Returns current step of the current :class:`Stage` of the :class:`Process` identified using *text*.
    This could be used to identify lower boundary of stepping loop.
    """
    Q1 = Process.objects.filter(name=text)
    if Q1:
        progress = Q1[0].getProgress()
        if not progress.progress:
            return 0
        return progress.progress
    return None

def getProcess(text):
    """
    Returns :class:`Process` identified by *text* and returns **None** if failed.
    """
    Q1 = Process.objects.filter(name=text)
    if Q1:
        return Q1[0]
    else:
        return None
    
def getProcessProgress(text):
    """
    Returns information related to the progress of the :class:`Process`.
    If process is already completed custom message will be sent. Otherwise
    returns dictionary consists of following keys.
    
    - process_name
    - process_description
    - stage_index
    - stage
    - progress
    - progress_boundary
    """
    Q1 = Process.objects.filter(name=text)
    if Q1:
        info = {}
        progress = Q1[0].getProgress()
        if progress.stage.index==0 and progress.progress==0 and progress.complete==1:
            return "Probably requested process may not have been started yet or it has been already closed."
        info['process_name'] = Q1[0].name
        info['process_description'] = Q1[0].description
        info['stage_index'] = progress.stage.index
        info['stage'] = progress.stage.stage_message
        info['progress'] = progress.progress
        info['progress_boundary'] = progress.complete
        return info
    return None