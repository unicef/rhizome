import subprocess,sys,time,pprint as pp
import traceback
from time import strftime

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from django.contrib.auth.models import User

from source_data.models import EtlJob, SourceDataPoint, ProcessStatus
from datapoints.models import Source
from source_data.etl_tasks.transform_odk import VcmSummaryTransform,VcmSettlementTransform
from source_data.etl_tasks.refresh_odk_work_tables import WorkTableTask
from source_data.etl_tasks.refresh_master import MasterRefresh

try:
    import source_data.prod_odk_settings as odk_settings
except ImportError:
    import source_data.dev_odk_settings as odk_settings

class EtlResource(ModelResource):

    class Meta():
        queryset = EtlJob.objects.all()
        resource_name = 'etl'
        always_return_data = True
        allowed_methods = ['get']

        authorization = Authorization()
        authentication = ApiKeyAuthentication()


    def get_object_list(self, request):
        '''this is the only method from tastypie that is overriden all logic
        for the etl api is dealt with inside this method'''

        task_string = request.GET['task']
        tic = strftime("%Y-%m-%d %H:%M:%S")

        ## stage the job ##
        created = EtlJob.objects.create(
            date_attempted = tic,
            task_name = task_string,
            status = 'PENDING'
        )

        ## MAKE THIS A CALL BACK FUNCTION ##
        et = EtlTask(task_string,created.guid)

        self.err, self.data = et.err, et.data

        print self.err, self.data

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

        print 'initializing etl task\n'

        self.task_guid = task_guid
        self.user_id = User.objects.get(username='odk').id

        self.function_mappings = {
              'test_api' : self.test_api,
              'odk_pull_vcm_summary_raw' : self.odk_pull_vcm_summary_raw,
              'odk_refresh_vcm_summary_work_table' : self.odk_refresh_vcm_summary_work_table,
              'odk_refresh_master' : self.odk_refresh_master,
              'odk_vcm_summary_to_source_datapoints': self.odk_vcm_summary_to_source_datapoints,
              }

        fn = self.function_mappings[task_string]

        self.err, self.data = fn()

    ###############################################################
    ########## METHODS BELOW USED BY API CALLS ABOVE ##############
    ###############################################################

    def test_api(self):

        try:
            data = 'API TEST IS WORKING'
        except Exception as err:
            return err, None

        return None, data


    def odk_pull_vcm_summary_raw(self):

        form_id = 'New_VCM_Summary'

        try:
            subprocess.call(['java','-jar',odk_settings.JAR_FILE,\
                '--form_id',form_id, \
                '--export_filename',form_id+'.csv', \
                '--aggregate_url',odk_settings.AGGREGATE_URL, \
                '--storage_directory',odk_settings.STORAGE_DIRECTORY, \
                '--export_directory',odk_settings.EXPORT_DIRECTORY, \
                '--odk_username',odk_settings.USERNAME, \
                '--odk_password',odk_settings.PASSWORD, \
                '--overwrite_csv_export' ,\
                '--exclude_media_export' \
              ])
        except Exception:
            err = traceback.format_exc()
            return err, None

        return None, 'Successfully Retrieved Data for form: ' + form_id

    def odk_refresh_vcm_summary_work_table(self):

        form_id = 'New_VCM_Summary'

        t = WorkTableTask(self.task_guid,form_id)
        err, data = t.main()

        return err, data

    def odk_vcm_summary_to_source_datapoints(self):

        v = VcmSummaryTransform(self.task_guid)
        v.vcm_summary_to_source_datapoints()

    def odk_refresh_master(self):

        try:
            source_datapoints = SourceDataPoint.objects.filter(
                status_id = ProcessStatus.objects.get(status_text='TO_PROCESS'),
                source_id = Source.objects.get(source_name='odk'))

            m = MasterRefresh(source_datapoints,self.user_id)
            m.main()

            dp_count = len(m.new_datapoints)
            success_msg = 'SUCSSFULLY CREATED: ' + str(dp_count) + ' NEW DATPOINTS'

        except Exception:
            err = traceback.format_exc()
            return err, None

        return None, success_msg
