from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sensors/$', views.sensors, name="sensors"),
    url(r'^actuators/$', views.actuators, name="actuators"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'ds18b20/$', views.ds18b20, name="ds18b20"),
    url(r'^json/(?P<type>(\w+))/(?P<id>[0-9]+)$', views.getLastData, name="getLastData")
]