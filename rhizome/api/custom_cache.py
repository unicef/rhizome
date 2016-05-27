from tastypie.cache import SimpleCache


class CustomCache(SimpleCache):
    '''
    Set up to override the simple cache method in order to customize the
    behavior of the cache control headers.
    '''

    def __init__(self, *args, **kwargs):
        super(CustomCache, self).__init__(*args, **kwargs)
        self.request = None
        self.response = None

    def cacheable(self, request, response):
        """
        Returns True or False if the request -> response is capable of being
        cached.
        """
        self.request = request
        self.response = response

        return bool(request.method == "GET" and response.status_code == 200)

    def cache_control(self):
        '''
        Instatiate the cache_control instance, and add the headers needed.
        '''

        cache_control = self.request.META.get('HTTP_CACHE_CONTROL')

        if cache_control is None:
            control = super(CustomCache, self).cache_control()
            control.update({'max_age': self.cache.default_timeout,
                            's-maxage': self.cache.default_timeout})
            return control
        else:
            self.response['Cache-Control'] = cache_control
            return {}
