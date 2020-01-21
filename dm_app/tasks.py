from celery.task import periodic_task
from datetime import timedelta

@periodic_task(run_every = timedelta(seconds = 60))
def test():
    print "is works!"
