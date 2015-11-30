from django.http import HttpResponseRedirect

class UserCheckMixin(object):
    '''
    Used to check if the user has functional permissions to perform what they
    are requesting to perform by virtue of the view associated with the URL.
    '''

    user_check_failure_path = ''  # can be path, url name or reverse_lazy

    def check_user(self, user):
        return True

    def user_check_failed(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.user_check_failure_path,'sorry you dont have permissions')

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)

class PermissionRequiredMixin(UserCheckMixin):
    '''
    Check if the user has permissions, and if they do not, bring them to the
    permissions_need page.
    '''
    user_check_failure_path = '/datapoints/permissions_needed'
    permission_required = None

    def check_user(self, user):
        return user.has_perm(self.permission_required)
