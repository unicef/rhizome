import os
import sys
import json
import urllib2
from urllib import urlencode

from datapoints.models import *

class DBRefreshTask(object):

    def __init__(self):

        print '...initializing...'

        self.base_url_string = 'http://polio.seedscientific.com/api/v2/'
        self.orm_mapper = {'campaign':Campaign}

    def main(self):

        for content_type, db_model in self.orm_mapper.iteritems():
            print 'processing_content_type: %s' % content_type
            api_data = self.api_wrapper(content_type)

    # def api_wrapper(self,kwargs=None,args=None):
    def api_wrapper(self,content_type):

        url_string = self.base_url_string + content_type
        response = urllib2.urlopen(url_string)
        x = response.read()


if __name__ == "__main__":
  db_r = DBRefreshTask()
  db_r.main()
