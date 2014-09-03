# from tastypie.resources import ModelResource,Resource, ALL
from tastypie.resources import ModelResource
from source_data.models import EtlJob



class EtlResource(ModelResource):
    '''Region Resource'''

    class Meta():
        queryset = EtlJob.objects.all()
        resource_name = 'etl'
        # authentication = ApiKeyAuthentication()
        # authorization = Authorization()

    # http://localhost:8000/api/v1/etl/?task=pull_odk
    def get_object_list(self, request):
        # run
        try:
            task = request.GET['task']
            et = EtlTask(task)
        except KeyError:
            return EtlJob.objects.all()

        return EtlJob.objects.all()


class EtlTask(object):
    '''one of three tasks in the data integration pipeline'''

    def __init__(self,task_string):
        print 'INITIALIZING ETL TASK\n' * 10

        self.function_mappings = {
              'pull_odk':self.pull_odk,
              'refresh_work_tables' : self.refresh_work_tables,
              'refresh_datapoints' : self.refresh_datapoints,
            }

        print task_string * 100

        fn = self.function_mappings[task_string]


    def pull_odk(self):


        status = 'COMPLETE'
        return status


    def refresh_work_tables(self):
        pass

    def refresh_datapoints(self):
        pass
