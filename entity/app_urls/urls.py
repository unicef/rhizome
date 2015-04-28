from django.conf.urls import url
from entity import views

urlpatterns = [

        ################
        ## DATAPOINTS ##
        ################

    ## (JSON FIXTURE) USER METADATA ##
    url(r'^users/metadata/$', views.api_user_mock,name='user_metadata'),

    ## USERS API ##
    url(r'^users/$', views.api_user, name='user'),

]
