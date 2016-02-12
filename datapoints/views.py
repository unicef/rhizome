from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse_lazy, reverse, resolve
from django.views import generic
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import user_passes_test
from django.template import Template, context, RequestContext
from django.shortcuts import get_object_or_404
from django.conf import settings

from datapoints.models import *
from datapoints.forms import *
from datapoints.mixins import PermissionRequiredMixin

from datapoints.pdf_utils import print_pdf
from waffle.decorators import waffle_switch
from rhizome.settings.base import STATICFILES_DIRS

def about(request):
    html = settings.ABOUT_HTML
    return render_to_response('about.html', {'html': html},
                              context_instance=RequestContext(request))


def export_file(request):
    file_type = request.GET['type']
    url = request.GET['path']
    file_name = 'dashboards.' + file_type
    css_file = 'file://' + STATICFILES_DIRS[0] + '/css/pdf.css'

    cookie = {}
    cookie['name'] = 'sessionid'
    cookie['value'] = request.COOKIES[cookie['name']]

    javascript_delay = '10000'

    if 'pdf' in file_type:
        options = {'orientation': 'Landscape', 'javascript-delay': javascript_delay, 'quiet': ' '}
        content_type = 'application/pdf'
    else:
        options = {'javascript-delay': javascript_delay, 'width': '1425', 'quality': '100', 'quiet': ' '}
        content_type = 'image/JPEG'

    pdf_content = print_pdf(type=file_type, url=url, output_path=None, options=options, cookie=cookie, css_file=css_file)

    if isinstance(pdf_content, IOError):
        response = HttpResponse(status=500)
    else:
        response = HttpResponse(content=pdf_content, content_type=content_type)
        response['Content-Disposition'] = 'attachment; filename=' + file_name

    response.set_cookie('fileDownloadToken', 'true')
    return response

## OPEN VIEWS ( needs authentication, but no specific permissions )##
def data_browser(request):
    return render_to_response('datapoints/index.html',\
        context_instance=RequestContext(request))

def dashboards(request):
    return render_to_response('dashboard-builder/list.html',
                              context_instance=RequestContext(request))

def charts(request):
    return render_to_response('charts/index.html',
                              context_instance=RequestContext(request))

def source_data(request):
    return render_to_response('source-data/index.html',
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
def chart_builder(request, chart_id=None):
    return render_to_response('charts/create.html', {'chart_id': chart_id},
                              context_instance=RequestContext(request))

@user_passes_test(lambda u: u.groups.filter(name='manage_system')\
    ,login_url='/datapoints/permissions_needed/',redirect_field_name=None)
def manage_system(request):
    return render_to_response('manage_system.html',\
        context_instance=RequestContext(request))

def update_campaign(request):
    return render_to_response('manage_system.html', context_instance=RequestContext(request))

class DashBoardView(generic.ListView):
    paginate_by = 50

    template_name = 'dashboard/index.html'
    context_object_name = 'user_dashboard'

    def get_queryset(self): ## not sure why this works. ##
        return DataPoint.objects.all()[:1]

class UserCreateView(PermissionRequiredMixin, generic.CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = UserCreateForm

    def get_success_url(self):
        new_user_id = self.object.id

        return reverse_lazy('datapoints:user_update',\
            kwargs={'pk':new_user_id})

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

    def form_valid(self, form):
        new_user = form.save()
        # set the user location permission just use the ajax call.
        # permission_obj = UserAdminLevelPermission.objects.get(user=new_user)
        # user_location_permission = LocationPermission.objects.get(user=new_user)
        # location = Location.objects.get(id=user_location_permission.top_lvl_location_id)
        # permission_obj.location_type = location.location_type
        # permission_obj.save()
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
