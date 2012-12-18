#!/usr/bin/python


from gearman import GearmanWorker

def speak(job):
    r = 'Hello %s' % job.arg
    print r
    return r

worker = GearmanWorker(["besrvuc-nag02"])
worker.register_task('speak', speak)
worker.work()
