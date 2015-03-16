from advanced.pickle import writePickle
from train.models import PrimaryTrain, Train
from schedule.models import PrimarySchedule, Schedule


def updateInitial():
    """
    Preparing for the update process based on server data.
    This will do emptying of auto generated **schedule_downloads**, 
    **schedule_formatted_data** pickles. It will update primary tables
    with secondary table information if primary tables are empty.
    """
    print("Updating process has started.")
    #if primary tables are empty atlest fill them with secondary data.
    if not PrimaryTrain.objects.count():
        Q1 = Train.objects.all()
        for i in Q1:
            Q2 = PrimaryTrain(number=i.number,
                              name = i.name,
                              start = i.start,
                              end = i.end,
                              start_time = i.start_time,
                              end_time = i.end_time,
                              end_time_days = i.end_time_days,
                              start_date = i.start_date,
                              end_date = i.end_date,
                              up = i.up,
                              comment = i.comment,
                              description = i.description,
                              type = i.type,
                              classes = i.classes,
                              frequency = i.frequency,
                              facilities = i.facilities)
            Q2.save()
    if not PrimarySchedule.objects.count():
        Q3 = Schedule.objects.all()
        for i in Q3:
            Q4 = Schedule(station = i.station,
                          train = i.train,
                          arrival = i.arrival,
                          departure = i.departure,
                          arrival_days = i.arrival_days,
                          departure_days = i.departure_days)
            Q4.save()
    
    writePickle("gen","schedule_downloads",[])
    writePickle("gen","schedule_formatted_data",[])
    