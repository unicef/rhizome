from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib.auth.models import User

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from polio.forms import UserForm


@login_required
def home(request):
    return HttpResponseRedirect('/datapoints')

class UserCreateView(generic.CreateView):
    model = User
    form_class = UserForm
    template_name = 'registration/create.html'
    success_url="/datapoints"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserCreateView, self).dispatch(*args, **kwargs)
