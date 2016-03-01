from django.contrib.auth.models import Group
from rhizome.api.resources.base_model import BaseModelResource

class GroupResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = Group.objects.all().values()
        resource_name = 'group'

