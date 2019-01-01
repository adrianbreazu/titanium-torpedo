from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sensors/$', views.sensors, name="sensors"),
    url(r'^actuators/$', views.actuators, name="actuators"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^ds18b20/$', views.ds18b20, name="ds18b20"),
    url(r'^store_data/$', views.store_sensor_data, name="store_sensor_data"),
    url(r'^json/(?P<type>(\w+))/(?P<iot_id>[0-9]+)$', views.getLastData, name="getLastData"),
    url(r'^json/(?P<iot_id>[0-9]+)$', views.getLastIotData, name='getLastIotData'),
    url(r'^clujbike/$', views.clujbike, name="clujbike"),
    url(r'^get_temp_data/$', views.getPeriodData, name="get_temp_data"),
    url(r'^get_iots/$', views.getIots, name="iots"),
    url(r'^getRelayStatus/$', views.getRelayStatus, name="/"),
    url(r'^setRelayStatus/$', views.setRelayStatus, name="set_relay_status"),
    url(r'^resetRelays/$', views.resetRelays, name="reset_relays"),
    url(r'^getPeriodIntervalData/$', views.getSensorDataForInterval, name="getPeriodIntervalData"),
    url(r'^getIotReadingErrors/$', views.getIotReadingErrors, name="getIotReadingErrors"),
]

handler404 = views.handler404