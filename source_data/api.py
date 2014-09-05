from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from source_data.models import EtlJob
from time import strftime

import subprocess
import sys

## FIX THIS!!!! NEED TO GET THIS INTO A BETTER CONF FILE
sys.path.append('/Users/johndingee_seed/code/polio/source_data/etl_tasks')
import odk_settings

class EtlResource(ModelResource):
    '''Region Resource'''

    class Meta():
        queryset = EtlJob.objects.all()
        resource_name = 'etl'
        always_return_data = True
        allowed_methods = ['get']

        authorization = Authorization()
        # authentication = ApiKeyAuthentication()

    # http://localhost:8000/api/v1/etl/?task=pull_odk
    def get_object_list(self, request):

        task_string = request.GET['task']
        print task_string
        tic = strftime("%Y-%m-%d %H:%M:%S")

        ## stage the job ##
        created = EtlJob.objects.create(
            date_attempted = tic,
            task_name = task_string,
            status = 'PENDING'
        )

        ## MAKE THIS A CALL BACK FUNCTION ##
        et = EtlTask(task_string,created.guid)

        return EtlJob.objects.filter(guid=created.guid)


class EtlTask(object):
    '''one of three tasks in the data integration pipeline'''

    def __init__(self,task_string,task_guid):

        print 'initializing etl task\n'

        self.task_guid = task_guid

        self.function_mappings = {
              'pull_odk' : self.pull_odk,
              'refresh_work_tables' : self.refresh_work_tables,
              'refresh_datapoints' : self.refresh_datapoints,
            }

        print task_string + '\n' * 100

        fn = self.function_mappings[task_string]
        fn()

    def pull_odk(self):

        for form_id in odk_settings.FORM_LIST:

            subprocess.call(['java','-jar',odk_settings.JAR_FILE,\
                '--form_id',form_id, \
                '--export_filename',form_id+'.csv', \
                '--aggregate_url',odk_settings.AGGREGATE_URL, \
                '--storage_directory',odk_settings.STORAGE_DIRECTORY, \
                '--export_directory',odk_settings.EXPORT_DIRECTORY, \
                '--odk_username',odk_settings.USERNAME, \
                '--odk_password',odk_settings.PASSWORD \
              ])

    def refresh_work_tables(self):

        print 'ODB IS ALIVE \n' * 10

    def refresh_datapoints(self):

        print 'ODB IS DEAD \n' * 10
