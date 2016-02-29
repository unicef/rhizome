from tastypie.resources import ALL

from rhizome.api.resources.base_model import BaseModelResource
from rhizome.models import IndicatorTag

class IndicatorTagResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        queryset = IndicatorTag.objects.all().values('id', 'parent_tag_id', 'tag_name', 'parent_tag__tag_name')
        resource_name = 'indicator_tag'
        filtering = {
            "id": ALL,
        }

    def get_object_list(self, request):
        try:
            tag_id = request.GET['id']
            return IndicatorTag.objects.filter(id=tag_id).values()
        except KeyError:
            return super(IndicatorTagResource, self).get_object_list(request)

    def obj_create(self, bundle, **kwargs):
        post_data = bundle.data

        try:
            id = int(post_data['id'])
            if id == -1:
                id = None
        except KeyError:
            id = None

        tag_name = post_data['tag_name']

        defaults = {
            'tag_name': tag_name
        }

        try:
            parent_tag_id = int(post_data['parent_tag_id'])
            defaults = {
                'tag_name': tag_name,
                'parent_tag_id': parent_tag_id
            }
        except KeyError:
            pass

        tag, created = IndicatorTag.objects.update_or_create(
            id=id,
            defaults=defaults
        )

        bundle.obj = tag
        bundle.data['id'] = tag.id

        return bundle

