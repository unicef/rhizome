
from django.conf.urls import url
from meta_map.views import IndicatorMapCreateView


urlpatterns = [
## CREATE ##
    url(r'^map_indicator/$', IndicatorMapCreateView.as_view(),name='create_datapoint'),
]
