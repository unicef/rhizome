import json
import StringIO
import urlparse

from django.core.serializers import json as djangojson
from pandas import DataFrame
from tastypie.serializers import Serializer

from datapoints.models import Campaign, Indicator, Location

class CustomJSONSerializer(Serializer):
    """Does not allow out of range float values
    (in strict compliance with the JSON specification).
    Instead replaces these values with NULL."""

    formats = ['json', 'urlencode']
    content_types = {
        'json': 'application/json',
        'urlencode': 'application/x-www-form-urlencoded',
        }

    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content):
        pass

    def to_json(self, data, options=None):

        options = options or {}
        data = self.to_simple(data, options)

        return djangojson.json.dumps(
            data,
            allow_nan=True,
            cls=NanEncoder,
            sort_keys=True,
            ensure_ascii=False)

class NanEncoder(djangojson.DjangoJSONEncoder):

    nan_str = 'null'

    def iterencode(self, o, _one_shot=False):
        """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = json.encoder.encode_basestring_ascii
        else:
            _encoder = json.encoder.encode_basestring
        if self.encoding != 'utf-8':
            def _encoder(o, _orig_encoder=_encoder, _encoding=self.encoding):
                if isinstance(o, str):
                    o = o.decode(_encoding)
                return _orig_encoder(o)

        def floatstr(o, allow_nan=self.allow_nan,
                _repr=json.encoder.FLOAT_REPR, _inf=json.encoder.INFINITY,
                _neginf=-json.encoder.INFINITY):
            # Check for specials.  Note that this type of test is processor
            # and/or platform-specific, so do tests which don't depend on the
            # internals.

            if o != o:
                text = self.nan_str
            elif o == _inf:
                text = 'Infinity'
            elif o == _neginf:
                text = '-Infinity'
            else:
                return _repr(o)

            if not allow_nan:
                raise ValueError(
                    "Out of range float values are not JSON compliant: " +
                    repr(o))

            return text


        if (_one_shot and json.encoder.c_make_encoder is not None
                and self.indent is None and not self.sort_keys):
            _iterencode = json.encoder.c_make_encoder(
                markers, self.default, _encoder, self.indent,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, self.allow_nan)
        else:
            _iterencode = json.encoder._make_iterencode(
                markers, self.default, _encoder, self.indent, floatstr,
                self.key_separator, self.item_separator, self.sort_keys,
                self.skipkeys, _one_shot)
        return _iterencode(o, 0)


class CustomSerializer(Serializer):
    formats = ['json', 'csv','urlencode']
    content_types = {
        'json': 'application/json',
        'csv': 'text/csv',
        'urlencode': 'application/x-www-form-urlencoded',
    }

    def from_urlencode(self, data,options=None):
        """ handles basic formencoded url posts """
        qs = dict((k, v if len(v)>1 else v[0] )
            for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencode(self,content):
        pass

    def to_csv(self, data, options=None):
        '''
        First lookup the metadata (campaign, location, indicator) and build a map
        cooresponding to id / name.  Afterwords iterate through the dataobjecst
        passed, unpack the indicator objects and create a dataframe which gets
        converted to a csv.
        '''

        # response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        options = options or {}
        data = self.to_simple(data, options)
        data_objects = data['objects']

        try:
            meta_lookup = self.build_meta_lookup(data_objects)
        except KeyError:
            ## a little bit of a hack, but this is the condition that for now
            ## alerts the system that this is a raw csv for a document_id.
            submission_data = [row['submission_json'] for row in data_objects]
            return self.clean_and_prep_csv(submission_data)

        expanded_objects = []

        for obj in data_objects:

            expanded_obj = {}

            expanded_obj['location'] = meta_lookup['location'][obj['location']]
            expanded_obj['campaign'] = meta_lookup['campaign'][obj['campaign']]

            for ind_dict in obj['indicators']:

                indicator_string = meta_lookup['indicator'][\
                    int(ind_dict['indicator'])]

                indicator_value = ind_dict['value']
                expanded_obj[indicator_string] = indicator_value

            expanded_objects.append(expanded_obj)

        csv = self.clean_and_prep_csv(expanded_objects)

        return csv

    def clean_and_prep_csv(self, data_objects):

        csv_df = DataFrame(data_objects)

        ## rearrange column order ( POLIO-200 ) ##
        ## http://stackoverflow.com/questions/13148429 ##
        cols = csv_df.columns.tolist()
        cols = cols[-2:] + cols[:-2]
        csv_df = csv_df[cols]

        csv = StringIO.StringIO(str(csv_df.to_csv(index=False)))

        return csv

    def build_meta_lookup(self,object_list):
        '''
        Instead of hitting the datbase every time you need to find the
        string for a particular meta data item.. build a dictionary
        once, store it in memory and access metadata values this way.

        '''
        # set up the lookup object
        meta_lookup = {'location':{},'campaign':{},'indicator':{}}

        ## find the location and campaign ids from the object list
        location_ids = [obj['location'] for obj in object_list]
        campaign_ids = [obj['campaign'] for obj in object_list]


        ## every object has all indicators, so find the first one, and the IDs
        ## for each indicator in that object

        indicator_nodes = [obj['indicators'] for obj in object_list]

        indicator_ids = []
        for ind in indicator_nodes:

            indicator_ids.extend([i['indicator'] for i in ind])

        for r in Location.objects.filter(id__in=location_ids):
            meta_lookup['location'][r.id] = r.__unicode__()

        for c in Campaign.objects.filter(id__in=campaign_ids):
            meta_lookup['campaign'][c.id] = c.__unicode__()

        for ind in Indicator.objects.filter(id__in=indicator_ids):
            meta_lookup['indicator'][ind.id] = ind.__unicode__()


        return meta_lookup
