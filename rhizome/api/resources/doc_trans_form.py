from rhizome.api.resources.base_model import BaseModelResource
from rhizome.api.exceptions import DatapointsException
from rhizome.models import Document
# from rhizome.etl_tasks.simple_upload_transform import SimpleDocTransform
from rhizome.etl_tasks.transform_upload import ComplexDocTransform

class DocTransFormResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        resource_name = 'transform_upload'

    def get_object_list(self, request):
        '''

        ## when you upload a file, step one is getting data into source submission
            ## --> DocTransform <-- ##

        ## Step two is translating form source_submission into datapoints
            ## --> REfreshMaster <----

        ## step three is aggregation
            ## agg refresh ##

        '''
        try:
            doc_id = request.GET['document_id']
        except KeyError:
            raise DatapointsException(message='Document_id is a required API param')
        # dt = DocTransform(request.user.id, doc_id)

        try:
            dt = ComplexDocTransform(request.user.id, doc_id)
            dt.main()
        except Exception as err:
            raise DatapointsException(message=err.message)

        mr = MasterRefresh(request.user.id, doc_id)
        mr.main()

        c_id_list = set(list(DataPoint.objects\
            .filter(source_submission__document_id = doc_id)\
            .values_list('campaign_id')))

        for c_id in doc_campaign_ids:
            ar = AggRefresh(c_id)
            ar.main()

        return Document.objects.filter(id=doc_id).values()
