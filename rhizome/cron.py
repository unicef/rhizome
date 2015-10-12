from django_cron import CronJobBase, Schedule
from datapoints.cache_tasks import CacheRefresh

class AggAndComputeDataPoint(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'rhizome.agg_and_compute_datapoint'    # a unique code

    def do(self):

        print '==REEFFRESSH=='
        cr = CacheRefresh()
