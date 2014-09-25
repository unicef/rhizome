import subprocess,sys,time

from time import strftime
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from django.contrib.auth.models import User

from source_data.models import EtlJob
from source_data.etl_tasks.transform_odk import VcmSummaryTransform,VcmSettlementTransform
from source_data.etl_tasks.refresh_odk_work_tables import WorkTableTask
from source_data.etl_tasks.refresh_master import MasterRefresh

try:
    import source_data.prod_odk_settings as odk_settings
except ImportError:
    import source_data.dev_odk_settings as odk_settings

class EtlResource(ModelResource):
    '''Region Resource'''

    class Meta():
        queryset = EtlJob.objects.all()
        resource_name = 'etl'
        always_return_data = True
        allowed_methods = ['get']

        authorization = Authorization()
        authentication = ApiKeyAuthentication()

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

        toc = strftime("%Y-%m-%d %H:%M:%S")
        created.date_completed = toc
        created.status = 'COMPLETE'

        created.save()

        return EtlJob.objects.filter(guid=created.guid)


class EtlTask(object):
    '''one of three tasks in the data integration pipeline'''

    def __init__(self,task_string,task_guid):

        print 'initializing etl task\n'

        self.task_guid = task_guid
        self.user_id = User.objects.get(username='odk').id

        x = task_string + '\n'

        self.function_mappings = {
              'odk_full_refresh' : self.odk_full_refresh,
              'odk_vcm_summary_refresh' : self.odk_vcm_summary_refresh,
              # 'refresh_odk_work_tables' : self.refresh_work_tables,
              # 'ingest_odk_vcm_summary' : self.ingest_odk_vcm_summary,
              # 'ingest_odk_vcm_settlement' : self.ingest_odk_vcm_settlement,
              # 'refresh_master' : self.refresh_master,
              'test_api' : self.test_api,
            }

        fn = self.function_mappings[task_string]

        fn()

    def odk_full_refresh(self):

        self.odk_pull_raw_form_data()
        self.odk_refresh_work_tables()


    def odk_vcm_summary_refresh(self):

        # self.odk_pull_raw_form_data('New_VCM_Summary')
        # self.odk_refresh_work_tables('New_VCM_Summary')

        vst = VcmSummaryTransform(self.task_guid)

        mappings = vst.pre_process_odk()
        source_dps = vst.vcm_summary_to_source_datapoints()

        results = self.refresh_master(mappings,source_dps)


    def odk_pull_raw_form_data(self,form_id=None):

        forms_to_pull = []

        if form_id:
            forms_to_pull.append(form_id)
        else:
            forms_to_pull = odk_settings.FORM_LIST


        for form_id in forms_to_pull:
            print form_id
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

    def odk_refresh_work_tables(self,form_id=None):

        forms_to_pull = []

        if form_id:
            forms_to_pull.append(form_id)
        else:
            forms_to_pull = odk_settings.FORM_LIST

        for source_file in forms_to_pull:
              print 'refreshing work table form: ' +  source_file

              t = WorkTableTask(self.task_guid,source_file)


    def odk_pre_transform(self):

        v = VcmTransform(self.task_guid)

    def ingest_odk_regions(self):

        v_sett_t = VcmSettlementTransform(self.task_guid)
        v_sett_t.refresh_source_regions()

    def refresh_master(self,mappings,source_datapoints):

        m = MasterRefresh(mappings,source_datapoints,self.user_id)
        m.main()

    def test_api(self):

        print 'API TEST IS WORKING \n' * 5
