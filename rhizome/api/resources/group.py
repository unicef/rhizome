from django.contrib.auth.models import Group
from rhizome.api.resources.base_model import BaseModelResource


class GroupResource(BaseModelResource):
    '''
    **GET Request** Returns the list of all groups in the application.
        - *Required Parameters:* 
                        none
    '''

    class Meta(BaseModelResource.Meta):
        queryset = Group.objects.all().values()
        resource_name = 'group'
