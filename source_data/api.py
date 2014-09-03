from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from source_data.models import EtlJob
from time import strftime



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

        et = EtlTask(task_string)

        return EtlJob.objects.filter(guid=created.guid)


class EtlTask(object):
    '''one of three tasks in the data integration pipeline'''

    def __init__(self,task_string):
        print 'initializing etl task\n'

        self.function_mappings = {
              'pull_odk':self.pull_odk,
              'refresh_work_tables' : self.refresh_work_tables,
              'refresh_datapoints' : self.refresh_datapoints,
            }

        fn = self.function_mappings[task_string]


    def pull_odk(self):

        status = 'COMPLETE'
        print 'I AM PULLING ODK!\n' * 10
        return status


    def refresh_work_tables(self):
        pass

    def refresh_datapoints(self):
        pass
