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
from source_data.etl_tasks.refresh_master import MasterRefresh

from datapoints import cache_tasks

try:
    import source_data.prod_odk_settings as odk_settings
except ImportError:
    import source_data.dev_odk_settings as odk_settings


class EtlResource(ModelResource):
    '''
    The ETL Resource is a Tastypie model resource, and as such, one record is
    inserted into the source_data_etljob table every time this class is
    instantiated.

    Furthermore, the 'get_object_list' function is overridden and the
    EtlTask is instantiated.  The EtlTask code takes the "task" parameter
    and prefroms the necessary data transformations.

    The cache_refresh, meta_datarefresh, and ODK refreshes are handled here,
    and because of which all of these specific tasks can be traced via the
    source_data_etljob table.
    '''

    class Meta():
        queryset = EtlJob.objects.all()
        resource_name = 'etl'
        always_return_data = True
        allowed_methods = ['get']
        filtering = {"cron_guid": ALL }

        authorization = Authorization()

    def get_object_list(self, request):
        '''
        This is the only method from tastypie that is overriden all logic
        for the etl api is dealt with inside this method.

        The crucial peice here to undestdand is how the etl_job is traced
        and how the data form the url is passed to the ETL engine.  For more
        on how this all works, take a look at the EtlTask() class.

        '''

        # required #
        task_string = request.GET['task']

        # optional #
        try:
            form_name = request.GET['form_name']
        except KeyError:
            form_name = None

        try:
            cron_guid = request.GET['job_id']
        except KeyError:
            cron_guid = 'no_job_id_provided'

        tic = strftime("%Y-%m-%d %H:%M:%S")

        # stage the job #
        created = EtlJob.objects.create(
            date_attempted = tic,
            task_name = task_string,
            cron_guid = cron_guid,
            status = 'PENDING'
        )

        # MAKE THIS A CALL BACK FUNCTION #
        et = EtlTask(task_string,created.guid,form_name)

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
    '''
    When instantiated, find the function appropriate for the task requested and
    execute that funciton, returning both 'Error', and 'Data' from each etl task
    '''

    def __init__(self,task_string,task_guid,form_name=None):

        self.task_guid = task_guid
        self.form_name = form_name
        self.user_id = User.objects.get(username='john').id

        self.function_mappings = {
            'test_api' : self.test_api,
            'start_odk_jar' :self.start_odk_jar,
            'finish_odk_jar' :self.finish_odk_jar,
            'refresh_cache': self.refresh_cache,
            'refresh_metadata': self.refresh_metadata_wrapper,
            'get_odk_forms_to_process': self.get_odk_forms_to_process,
            }

        fn = self.function_mappings[task_string]

        self.err, self.data = fn()


    ###############################################################
    ########## METHODS BELOW USED BY API CALLS ABOVE ##############
    ###############################################################


    def test_api(self):
        '''
        Basic endpoint to test the functionlaity of the ETL apo
            - /api/v1/etl/?task=test_api
        '''

        try:
            data = 'API TEST IS WORKING'
        except Exception as err:
            return err, None

        return None, data


    def refresh_cache(self):
        '''
        When dealing with the cache_refresh task in the etl api, instantiate the
        CacheRefresh class.  This is precisely the same function as clicking the
        "refresh_cache" button on the cache_control page, but having it in the
        ETL api allows this functionality to be engaged by a cron job or rest
        API.
        '''
        try:
            cr = cache_tasks.CacheRefresh()
        except Exception as err:
            return err, None

        data = 'complete'

        return None, data

    def refresh_metadata_wrapper(self):
        '''
        Certain metadata resources have additional iformation that is not
        stored directly at that model.  For instance, indicators have bounds
        and tags associated to them.. both many to many, and in order to have
        direct access to that information when the api request comes in, we
        store this infomration in the indicator_abstracted table, which hodls
        as json all of the data needed by the API.

        In order to have this information immediately avaiable to the API, we
        run the "refresh_metadata" task that will transform and cache metadata
        in the format the api needs.

        Currently the two resource are abstracted in this manner:
            - user -> user_abstracted
            - indicator -> indicator_abstracted
        '''

        try:
            meta_results = refresh_metadata
        except Exception as err:
            return err, None

        data = 'complete'

        return None, data


    def start_odk_jar(self):
        '''
        This tells the system that the Jar file process has been initated.
        When this is complete, the system calls "finish_odk_jar."
        '''

        try:
            data = 'Starting to Pull data from ODK Aggregate...'
        except Exception as err:
            return err, None

        return None, data


    def finish_odk_jar(self):
        '''
        An indication to the system that the odk jar file process is complete.
        Haivng these two endpoitns tracked at either side of the jar file
        execution allows us to see how long each form takes to pull down from
        the ODK aggregate server.
        '''

        try:
            data = 'Done to Pulling data from ODK Aggregate!'
        except Exception as err:
            return err, None

        return None, data


    def get_odk_forms_to_process(self):
        '''
        Look up ( via the etl API ), the forms that the system requires us to
        look up data for.  The forms that need to be processed are in the
        odk_form table.  Having a row in here causes the system to go out and
        get data for the forms specified and transform it to source datapoints
        and finally datapoints.

        TO DO - pull this from document metadata.
        '''

        odk_form_list = ODKForm.objects.all().values_list('form_name',flat=True)
        cleaned_forms = [str(x) for x in odk_form_list]

        return None, cleaned_forms
