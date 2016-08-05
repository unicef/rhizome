from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.simple_models import UserGroup


class UserGroupResource(BaseModelResource):
    '''
    **GET Request** Returns the list of all user_groups in the application unless an optional parameter is specified
        - *Optional Parameters:*
            'user_id' the id of the user for which we want to get user groups
    **POST Request** Create a user->group assignment
        -*Required Parameters:*
            'user_id'
            'group_id'
        -*Errors*
            The api returns a 500 error if any of the required parameters are missing
    **DELETE Request**
        -*Required Parameters:*
            'user_id'
            'group_id'
        -*Errors*
            The api returns a 500 error if any of the required parameters are missing
    '''

    class Meta(BaseModelResource.Meta):
        object_class = UserGroup
        resource_name = 'user_group'
        filtering = {
            'user_id': ALL,
            'group_id': ALL
        }
        required_fields_for_post = ['user_id', 'group_id']
