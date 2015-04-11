from traceback import format_exc
from time import strftime

from tastypie.constants import ALL
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from django.contrib.auth.models import User

from source_data.models import *
from source_data.etl_tasks.transform_odk import VcmSummaryTransform
from source_data.etl_tasks.refresh_odk_work_tables import WorkTableTask
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks import ingest_polygons

from datapoints.models import Source
from datapoints.cache_tasks import CacheRefresh


class EtlResource(ModelResource):

    class Meta():
        queryset = EtlJob.objects.all()
        resource_name = 'etl'
        always_return_data = True
        allowed_methods = ['get']
        filtering = {"cron_guid": ALL }

        authorization = Authorization()
        # authentication = ApiKeyAuthentication()


    def get_object_list(self, request):
        '''
        This is the only method from tastypie that is overriden all logic
        for the etl api is dealt with inside this method

        Fix placeholder guid!

        '''

        ## http://localhost:8000/api/v1/etl/?task=odk_refresh_vcm_summary_work_table&cron_guid=john_is_testing

        task_string = request.GET['task']
        cron_guid = 'placeholder_guid'#request.GET['cron_guid']

        tic = strftime("%Y-%m-%d %H:%M:%S")

        ## stage the job ##
        created = EtlJob.objects.create(
            date_attempted = tic,
            task_name = task_string,
            cron_guid = cron_guid,
            status = 'PENDING'
        )

        ## MAKE THIS A CALL BACK FUNCTION ##
        et = EtlTask(task_string,created.guid)

        self.err, self.data = et.err, et.data

        toc = strftime("%Y-%m-%d %H:%M:%S")
        created.date_completed = toc

        if self.err:
            created.status = 'ERROR'
            created.error_msg = self.err

        elif self.data:
            created.status = 'COMPLETE'
            created.success_msg = self.data

        created.save()

        return EtlJob.objects.filter(guid=created.guid)


class EtlTask(object):
    '''one of three tasks in the data integration pipeline'''

    def __init__(self,task_string,task_guid):

        self.task_guid = task_guid
        self.user_id = User.objects.get(username='odk').id

        self.function_mappings = {
            'test_api' : self.test_api,
            'odk_refresh_vcm_summary_work_table' : self.odk_refresh_vcm_summary_work_table,
            'odk_vcm_summary_to_source_datapoints': self.odk_vcm_summary_to_source_datapoints,
            'odk_refresh_master' : self.odk_refresh_master,
            'start_odk_jar' :self.start_odk_jar,
            'finish_odk_jar' :self.finish_odk_jar,
            'refresh_cache': self.refresh_cache,
            }

        fn = self.function_mappings[task_string]

        self.err, self.data = fn()

    ###############################################################
    ########## METHODS BELOW USED BY API CALLS ABOVE ##############
    ###############################################################


    def parse_geo_json(self):

        err, data = ingest_polygons.main()

        return err, data


    def test_api(self):
        '''
        '''

        try:
            data = 'API TEST IS WORKING'
        except Exception as err:
            return err, None

        return None, data


    def refresh_cache(self):
        '''
        datapoint -> agg_datapoint -> datapoint_with_computed
        '''
        try:
            cr = CacheRefresh()
        except Exception as err:
            return err, None

        data = 'complete' #cr.response_msg

        return None, data


    def start_odk_jar(self):
        '''
        '''

        try:
            data = 'Starting to Pull data from ODK Aggregate...'
        except Exception as err:
            return err, None

        return None, data


    def finish_odk_jar(self):
        '''
        '''

        try:
            data = 'Done to Pulling data from ODK Aggregate!'
        except Exception as err:
            return err, None



        return None, data


    def odk_refresh_vcm_summary_work_table(self):
        '''
        '''

        form_id = 'New_VCM_Summary'

        t = WorkTableTask(self.task_guid,form_id)
        err, data = t.main()

        return err, data

    def odk_vcm_summary_to_source_datapoints(self):
        '''
        '''

        v = VcmSummaryTransform(self.task_guid)
        err, data = v.vcm_summary_to_source_datapoints()

        return err, data

    def odk_refresh_master(self):
        '''
        '''

        try:
            source_datapoints = SourceDataPoint.objects.filter(
                status_id = ProcessStatus.objects.get(status_text='TO_PROCESS'),
                source_id = Source.objects.get(source_name='odk'))

            m = MasterRefresh(source_datapoints,self.user_id)
            m.main()

            dp_count = len(m.new_datapoints)
            success_msg = 'SUCSSFULLY CREATED: ' + str(dp_count) + ' NEW DATPOINTS'

        except Exception:
            err = format_exc()
            return err, None

        return None, success_msg
