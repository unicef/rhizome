from pandas import DataFrame

from datapoints.models import DataPoint


def full_cache_refresh():

    indicators = set(list(DataPoint.objects.all()\
        .values_list('indicator_id',flat=True)))


    indicator_df = DataFrame(columns = indicators)

    print indicator_df

    print indicators
