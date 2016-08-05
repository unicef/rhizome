from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import RhizomeApiException
from rhizome.simple_models import CustomDashboard, CustomChart

import json


class CustomDashboardResource(BaseModelResource):
    '''
    **GET Requests:** Get a dashboard. If no params are passed, returns all the dashboards
        - *Optional Parameters:*
            'id'
    **GET Request get detail:**
        - to access a specific chart, send a get request to /api/v1/custom_dashboard/<dashboard_id>/
    **POST Requests:** Create a dashboard
        - *Required Parameters:*
            'title'
        - *Optional Parameters:*
            'chart_uuids': this associates the given chart() with a dashboard
        - *Errors:*
            If a title is not supplied. The API will return a 500 error.
    **DELETE Requests:** There are two ways to submit a delete request to API
        - to delete a resource, HTTP delete request to /api/v1/custom_dashboard/<dashboard_id>/
    '''
    class Meta(BaseModelResource.Meta):
        object_class = CustomDashboard
        resource_name = 'custom_dashboard'
        filtering = {
            "id": ALL,
        }
        always_return_data = True
        required_fields_for_post = ['title']

    def get_detail(self, request, **kwargs):
        '''
        This method gives the chart data for each dashboard so that we can
        see all of the information needed to render a dashboard by accessing
        that uri.

        The custom dashboard model stores on it "rows" each of wiht have a
        "layout" and a number of chart_uuids.

        In this method, we iterate through the chart_uuids and add the chart
        objects to the response.

        Since this is not a simple matter of just hitting the database for
        an ID, and returning that object, we override the "get_detail" method
        here to return the related information for the resource.
        '''

        requested_id = kwargs['pk']
        bundle = self.build_bundle(request=request)
        response_data = CustomDashboard.objects.get(id=requested_id).__dict__
        response_data.pop('_state')

        if response_data['rows']:
            response_data_rows = response_data['rows']
            chart_uuids = []
            for row in response_data_rows:
                chart_uuids = chart_uuids + (row['charts'])
            charts = list(CustomChart.objects.filter(uuid__in=chart_uuids))

            # create a dict to get random access
            charts_dict = {}
            for chart in charts:
                chart_dict = chart.__dict__
                chart_dict.pop('_state')
                charts_dict[chart.uuid] = chart_dict

            # add the charts to the row in the response
            for idx, row in enumerate(response_data_rows):
                charts_list = row['charts']
                for idx2, chart_uuid in enumerate(charts_list):
                    if chart_uuid in charts_dict.keys():
                        chart = charts_dict[chart_uuid]
                        response_data_rows[idx]['charts'][idx2] = chart

            response_data['rows'] = response_data_rows

        bundle.data = response_data
        return self.create_response(request, bundle)
