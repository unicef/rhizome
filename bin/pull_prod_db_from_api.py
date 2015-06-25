#!/usr/cat /hom bin/python

import sys
import json
import urllib2
import subprocess
from time import sleep
from urllib import urlencode
from uuid import uuid4

class DBRefreshTask(object):

    def __init__(self):

        print '...initializing...'

    def main(self):

        print 'MAIN FUNCTION!'

        forms_to_process = [1,2,3]

        for form in forms_to_process:
            print 'processing_forms: %s' % form

    def api_wrapper(self,kwargs=None):

        kwargs['job_id'] = self.cron_guid
        url_string = self.base_url_string + '?' + urlencode(dict(**kwargs))
        response = urllib2.urlopen(url_string)#
        etl_api_response = json.loads(response.read())['objects'][0]

        return etl_api_response

if __name__ == "__main__":
  db_r = DBRefreshTask()
  db_r.main()
