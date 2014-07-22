from django.http import HttpResponseRedirect

class UserCheckMixin(object):
    user_check_failure_path = ''  # can be path, url name or reverse_lazy

    def check_user(self, user):
        return True

    def user_check_failed(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.user_check_failure_path,'sorry you dont have permissions bro!')

    def dispatch(self, request, *args, **kwargs):
        if not self.check_user(request.user):
            return self.user_check_failed(request, *args, **kwargs)
        return super(UserCheckMixin, self).dispatch(request, *args, **kwargs)

class PermissionRequiredMixin(UserCheckMixin):
    user_check_failure_path = '/datapoints/permissions_needed'
    permission_required = None

    def check_user(self, user):
        return user.has_perm(self.permission_required)
