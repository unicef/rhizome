from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy, reverse, resolve
from django.views import generic
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test

from django.template import RequestContext

from pandas import DataFrame
from datapoints.models import *
from datapoints.forms import *
from datapoints import agg_tasks
from datapoints import cache_meta
from datapoints.mixins import PermissionRequiredMixin


## OPEN VIEWS ( needs authentication, but no specific permissions )##
def data_browser(request):
    return render_to_response('datapoints/index.html',\
        context_instance=RequestContext(request))

def dashboard_list(request):
    return render_to_response('dashboard-builder/list.html',
                              context_instance=RequestContext(request))

### PERMISSION RESTRICTED VIEWS ###

@user_passes_test(lambda u: u.groups.filter(name='data_entry')\
    ,login_url='/datapoints/permissions_needed/',redirect_field_name=None)
def data_entry(request):
    return render_to_response('data-entry/index.html',
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.groups.filter(name='dashboard_builder')\
    ,login_url='/datapoints/permissions_needed/',redirect_field_name=None)
def dashboard_builder(request, dashboard_id=None):
    return render_to_response('dashboard-builder/index.html', {'dashboard_id': dashboard_id},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.groups.filter(name='dashboard_builder')\
    ,login_url='/datapoints/permissions_needed/',redirect_field_name=None)
def chart_builder(request, dashboard_id):
    return render_to_response('dashboard-builder/chart_builder.html', {'dashboard_id': dashboard_id},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.groups.filter(name='manage_system')\
    ,login_url='/datapoints/permissions_needed/',redirect_field_name=None)
def manage_system(request):
    return render_to_response('manage_system.html',\
        context_instance=RequestContext(request))

class DashBoardView(generic.ListView):
    paginate_by = 50

    template_name = 'dashboard/index.html'
    context_object_name = 'user_dashboard'

    def get_queryset(self): ## not sure why this works. ##
        return DataPoint.objects.all()[:1]


class CampaignCreateView(PermissionRequiredMixin, generic.CreateView):
    model = Campaign
    success_url = '/manage_system/campaigns'
    template_name = 'campaigns/create.html'
    fields = ['office', 'campaign_type', 'start_date', 'end_date']


class CampaignUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = Campaign
    success_url = '/manage_system/campaigns'
    template_name = 'campaigns/update.html'
    form_class = CampaignForm


class UserCreateView(PermissionRequiredMixin, generic.CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = UserCreateForm

    def get_success_url(self,new_user_id):
        return reverse_lazy('datapoints:user_update',\
            kwargs={'pk':new_user_id})

    def form_valid(self, form):
        new_user = form.save()
        location_type = form.cleaned_data.get('location_type')
        UserAdminLevelPermission.objects.create(
            user=new_user,location_type=location_type
        )

        return HttpResponseRedirect(self.get_success_url(new_user.id))

class UserEditView(PermissionRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'user_edit.html'
    form_class = UserEditForm

    def dispatch(self, *args, **kwargs):
        return super(UserEditView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        requested_user_id = self.get_object().id
        return reverse_lazy('datapoints:user_update',\
            kwargs={'pk':requested_user_id})

    def get_context_data(self, **kwargs):
        context = super(UserEditView, self).get_context_data(**kwargs)
        user_obj = self.get_object()
        context['user_id'] = user_obj.id

        return context

    def get_initial(self):
        user_obj = self.get_object()
        lt = UserAdminLevelPermission.objects.get(user = user_obj).location_type
        return { 'location_type': lt }

    def form_valid(self, form):

        new_user = form.save()
        permission_obj = UserAdminLevelPermission.objects.get(user=new_user)
        form_location_type = form.cleaned_data.get('location_type')
        permission_obj.location_type = form_location_type
        permission_obj.save()


        return HttpResponseRedirect(self.get_success_url())


def html_decorator(func):
    """
    This decorator wraps the output of the django debug tooldbar in html.
    (From http://stackoverflow.com/a/14647943)
    """

    def _decorated(*args, **kwargs):
        response = func(*args, **kwargs)

        wrapped = ("<html><body>",
                   response.content,
                   "</body></html>")

        return HttpResponse(wrapped)

    return _decorated


@html_decorator
def debug(request):
    """
    Debug endpoint that uses the html_decorator,
    """
    path = request.META.get("PATH_INFO")
    api_url = path.replace("debug/", "")

    view = resolve(api_url)

    accept = request.META.get("HTTP_ACCEPT")
    accept += ",application/json"
    request.META["HTTP_ACCEPT"] = accept

    res = view.func(request, **view.kwargs)
    return HttpResponse(res._container)
