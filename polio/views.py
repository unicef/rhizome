from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.contrib.auth.models import User
from stronghold.decorators import public
from polio.forms import UserForm
from django.utils.decorators import method_decorator


def home(request):
    return HttpResponseRedirect('/datapoints')

class UserCreateView(generic.CreateView):
    model = User
    form_class = UserForm
    template_name = 'registration/create.html'
    success_url="/datapoints"

    @method_decorator(public)
    def dispatch(self, *args, **kwargs):
        return super(UserCreateView, self).dispatch(*args, **kwargs)