from django_cron import CronJobBase, Schedule
from django.contrib.auth.models import User

from datapoints.cache_tasks import CacheRefresh

from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.models import SourceSubmission

class AggAndComputeDataPoint(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'rhizome.agg_and_compute_datapoint'    # a unique code

    def do(self):
        cr = CacheRefresh()

class MasterRefreshJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'rhizome.master_refresh_job'    # a unique code

    def do(self):
        user_id = User.objects.get(username = 'cron').id
        document_id = SourceSubmission.objects.\
            filter(process_status='TO_PROCESS').\
            values_list('document_id',flat=True)[0]

        print 'DOCUMENT_ID: %s' % document_id

        mr = MasterRefresh(user_id, document_id)
        mr.main()
