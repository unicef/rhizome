from django.conf import settings
from django.middleware.csrf import _sanitize_token, constant_time_compare
from django.utils.http import same_origin

from tastypie.authentication import SessionAuthentication


class CustomSessionAuthentication(SessionAuthentication):

    def is_authenticated(self, request, **kwargs):

        # this is the line i have to override in order to get
        # POST request to successfully authenticate ##
        if request.method in ['GET', 'POST', 'PATCH', 'DELETE']:
            return request.user.is_authenticated()

        if getattr(request, '_dont_enforce_csrf_checks', False):
            return request.user.is_authenticated()

        csrf_token = _sanitize_token(
            request.COOKIES.get(settings.CSRF_COOKIE_NAME, ''))

        if request.is_secure():
            referer = request.META.get('HTTP_REFERER')

            if referer is None:
                return False

            good_referer = 'https://%s/' % request.get_host()

            if not same_origin(referer, good_referer):
                return False

        request_csrf_token = request.META.get('HTTP_X_CSRFTOKEN', '')

        if not constant_time_compare(request_csrf_token, csrf_token):
            return False

        return request.user.is_authenticated()
