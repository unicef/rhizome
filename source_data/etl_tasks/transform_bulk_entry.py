
from source_data.models import SourceDataPoint

def bulk_data_to_sdps(some_data):
    print some_data

    source_datapoints = SourceDataPoint.objects.all()[:5]
    not_parsed = { 'r':'q' }

    return source_datapoints, not_parsed
