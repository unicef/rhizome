from datapoints.models import Location, LocationPermission, LocationTree

def get_locations_to_return_from_url(request):
    '''
    This method is used in both the /geo and /datapoint endpoints.  Based
    on the values parsed from the URL parameters find the locations needed
    to fulfill the request based on the four rules below.

    1. location_id__in =
    2. parent_location_id__in =

    right now -- this only filters if there is no param.. i should get the
    permitted locations first then do an intersection with the params..
    '''

    try:
        location_ids = request.GET['location_id__in'].split(',')
        return location_ids
    except KeyError:
        pass

    try:
        pl_id_list = request.GET['parent_location_id__in'].split(',')
        location_ids = list(Location.objects\
                    .filter(parent_location_id__in=pl_id_list)
                    .values_list('id',flat=True))
        location_ids.extend(pl_id_list)
        return location_ids
    except KeyError:
        pass

    ## if no params passed, return what user can see ##
    top_lvl_location_id = LocationPermission.objects\
        .get(user_id=request.user.id).top_lvl_location_id

    location_qs = (
        LocationTree.objects
        .filter(parent_location_id=top_lvl_location_id)
        .values_list('location_id', flat=True)
    )

    return location_qs

# This function does not seem to be used anywhere. Lets delete unless there something i missed - Dima
def clean_post_data(post_data_dict):
    cleaned = {}
    for k, v in post_data_dict.iteritems():
        to_clean = v[0]
        cleaned_v = to_clean.replace("[u'", "").replace("]", "")
        cleaned[k] = cleaned_v

    return cleaned
