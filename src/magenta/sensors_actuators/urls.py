from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sensors/$', views.sensors, name="sensors"),
    url(r'^actuators/$', views.actuators, name="actuators"),
    url(r'^dashboard/$', views.dashboard, name="dashboard")
]