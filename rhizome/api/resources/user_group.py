from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import UserGroup


class UserGroupResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = UserGroup.objects.all().values()
        resource_name = 'user_group'

    def obj_create(self, bundle, **kwargs):

        new_obj = UserGroup.objects.create(**bundle.data)
        bundle.obj = new_obj
        bundle.data['id'] = new_obj.id

        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        """
        """
        user_id = int(bundle.request.GET[u'user_id'])
        group_id = int(bundle.request.GET[u'group_id'])
        UserGroup.objects.filter(user_id=user_id, group_id=group_id)\
            .delete()

    def get_object_list(self, request):

        try:
            user_id = request.GET['user_id']
            return UserGroup.objects \
                .filter(user_id=user_id).values()
        except KeyError:
            return UserGroup.objects.all().values()
