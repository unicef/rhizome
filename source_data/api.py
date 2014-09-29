import subprocess,sys,time,pprint as pp
import traceback

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
              'odk_refresh_vcm_summary' : self.odk_refresh_vcm_summary,
              'odk_refresh_regions' : self.odk_refresh_regions,
              'odk_refresh_all' : self.odk_refresh_all,
            }

        fn = self.function_mappings[task_string]

        self.err, self.data = fn()


    def test_api(self):

        try:
            data = 'API TEST IS WORKING'
        except Exception as err:
            return err, None

        return None, data


    def odk_refresh_vcm_summary(self):

        try:
            results = {}

            # ## PULL THE ODK DATA FROM APP ENGINE ##
            # self.odk_pull_raw_form_data('New_VCM_Summary')

            # ## DUMP THE ODK DATA INTO THE WORK TABLE ##
            # self.odk_refresh_work_tables('New_VCM_Summary')

            ## CREATE AN OBJECT FOR A VCM SUMMARY TRANSFORMATION ##
            vst = VcmSummaryTransform(self.task_guid)

            ## PREPROCESS THIS DATA, THAT IS FIND THE META DATA MAPPINGS ##
            mappings = vst.pre_process_odk()

            ## CREATE SOURCE DPS FROM WHAT WE INSERTED INTO THE WORK TABLE ##
            vst.vcm_summary_to_source_datapoints()
            source_dps = vst.source_datapoint[:10]
            results['new_source_datapoint_count'] = self.handle_results(source_dps)

            ## FINALLY GET ALL DATAPOINTS BASED ON MAPPINGS AND SOURCE DPs ##
            dps = self.refresh_master(mappings,source_dps)
            results['new_datapoint_count'] = self.handle_results(dps)

            return None, results

        except Exception:
            err = traceback.format_exc()
            return err, None

    def odk_refresh_regions(self):

        v_sett_t = VcmSettlementTransform(self.task_guid)
        v_sett_t.refresh_source_regions()


    def odk_refresh_all(self):

        self.odk_pull_raw_form_data()
        self.odk_refresh_work_tables()


    ######################################################################
    ########## HELPER METHODS BELOW USED BY API CALLS ABOVE ##############
    ######################################################################

    def handle_results(self,objects):

        if objects:
            return len(objects)
        else:
            return 0


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


    def refresh_master(self,mappings,source_datapoints):

        m = MasterRefresh(mappings,source_datapoints,self.user_id)
        m.main()

        return m.new_datapoints
