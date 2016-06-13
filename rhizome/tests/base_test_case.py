from tastypie.test import ResourceTestCase


class RhizomeApiTestCase(ResourceTestCase):
    '''
    Subclassing all of the methods here

    https://github.com/django-tastypie/django-tastypie/blob/master/tastypie/test.py

    So that, in a basic api case, if there are no failiures we don't print
    the error... if there is, and the http codes don't match with what is
    expected, we print out the error message in order to make it easier on the
    developer debugging.

    Thus, we ask if you write a test against the api, please first ensure that
    you assert one of the methods below.. for instance, a GET, you just say,
    `self.assertHttpOK()` before you make any other assertions about what that
    data or error message is supposed to contain or represent.
    '''

    def printResponseIfError(self, resp, status_code):

        if resp.status_code != status_code:
            print '==\n' * 10
            print '==-error-==\n %s ' % self.deserialize(resp)

    def assertHttpOK(self, resp, status_code=200):
        self.printResponseIfError(resp, status_code)
        self.assertHttp(resp, status_code)

    def assertHttpCreated(self, resp, status_code=201):
        self.printResponseIfError(resp, status_code)
        self.assertHttp(resp, status_code)

    def assertHttpApplicationError(self, resp, status_code=500):
        self.printResponseIfError(resp, status_code)
        self.assertHttp(resp, status_code)

    def assertHttpUnprocessableEntity(self, resp, status_code=422):
        self.printResponseIfError(resp, status_code)
        self.assertHttp(resp, status_code)

    def assertHttp(self, resp, status_code):

        self.printResponseIfError(resp, status_code)
        self.assertEqual(resp.status_code, status_code)
