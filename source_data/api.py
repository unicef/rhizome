from pprint import pprint
from traceback import format_exc
from time import strftime

from tastypie.constants import ALL
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import ApiKeyAuthentication
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.conf import settings
from pandas import read_csv

from source_data.models import *
from source_data.etl_tasks.transform_odk import VcmSummaryTransform
from source_data.etl_tasks.refresh_master import MasterRefresh
from source_data.etl_tasks import ingest_polygons

from datapoints.models import Source
from datapoints import cache_tasks

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
        filtering = {"cron_guid": ALL }

        authorization = Authorization()
        authentication = ApiKeyAuthentication()


    def get_object_list(self, request):
        '''
        This is the only method from tastypie that is overriden all logic
        for the etl api is dealt with inside this method

        Fix placeholder guid!

        '''

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

        print et.err

        self.err, self.data = et.err, et.data


        toc = strftime("%Y-%m-%d %H:%M:%S")
        created.date_completed = toc

        if self.err:
            created.status = 'ERROR'
            created.error_msg = self.err
            created.save()

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
            # 'odk_refresh_vcm_summary_work_table' : self.odk_refresh_vcm_summary_work_table,
            # 'odk_vcm_summary_to_source_datapoints': self.odk_vcm_summary_to_source_datapoints,
            'odk_refresh_master' : self.odk_refresh_master,
            'start_odk_jar' :self.start_odk_jar,
            'finish_odk_jar' :self.finish_odk_jar,
            'ingest_odk_regions' :self.ingest_odk_regions,
            'refresh_cache': self.refresh_cache,
            'refresh_metadata': self.refresh_metadata,
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
            cr = cache_tasks.CacheRefresh()
        except Exception as err:
            return err, None

        data = 'complete' #cr.response_msg

        return None, data

    def refresh_metadata(self):
        '''
        user -> user_abstracted
        indicator -> indicator_abstracted
        '''

        try:
            indicator_cache_data = cache_tasks.cache_indicator_abstracted()
            user_cache_data = cache_tasks.cache_user_abstracted()
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


    def ingest_odk_regions(self):
        '''
        From the VCM settlements CSV ingest new reigions
        '''

        region_document, created = Document.objects.get_or_create(
            docfile = '',
            doc_text = 'VCM_Sett_Coordinates_1_2.csv',
            defaults = {
                'created_by_id':1, # john
                'source_id':Source.objects.get(source_name = 'odk').id
            }
        )

        region_document_id = region_document.id

        try:
            csv_root = settings.BASE_DIR + '/source_data/ODK/odk_source/csv_exports/'
            region_df = read_csv(csv_root + 'VCM_Sett_Coordinates_1_2.csv')
        except IOError:
            csv_root = settings.BASE_DIR + '/polio/source_data/ODK/odk_source/csv_exports/'
            region_df = read_csv(csv_root + 'VCM_Sett_Coordinates_1_2.csv')

        ## Convert to Work Table ##
        list_of_dicts = region_df.transpose().to_dict()

        for ix, d in list_of_dicts.iteritems():
             lower_dict = {}

             for k,v in d.iteritems():
                 lower_dict[k.lower().replace('-','_')] = v
                 lower_dict['process_status_id'] = 1
             try:
                 VCMSettlement.objects.create(**lower_dict)
             except IntegrityError as err:
                 print err
                 pass

        ## Merge Work Table Data into source_region / region / region_map ##

        sr = SourceRegion.objects.raw('''SELECT * FROM fn_sync_odk_regions(%s)
            ''',[region_document_id])

        data = [s.id for s in sr]

        return None, data
