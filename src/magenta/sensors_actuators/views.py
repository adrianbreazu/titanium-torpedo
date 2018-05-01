from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
import json
import datetime
import requests

from .models import ReadValue, IoT


def sensors(request):
    try:

        return HttpResponse("hey there you are on the sensors page")
    except Exception as e:
        print("error on dashboard: {0}".format(e))
    finally:
        print("done with dashboard")


def actuators(request):
    return render(request=request,
                  template_name="sensors_actuators/actuators.html")


def dashboard(request):
    type = "temperature"
    context = {}

    context['iot_objects'] = ReadValue.objects.filter(type=type).order_by('-datetime')[:20]

    context["title"] = "Dashboard"

    return render(request=request,
                  context=context,
                  template_name="sensors_actuators/index.html")


@csrf_exempt
def getIots(request):
    data = {}
    if request.method == "POST":
        try:
            iots= IoT.objects.filter(status="active").order_by("id")
            array = []
            for iot in iots:
                msg = {}
                msg['id'] = iot.id
                msg['type'] = iot.type
                msg['name'] = iot.name
                msg['location'] = iot.location
                msg['description'] = iot.description
                array.append(msg)
            data['iot'] = array

            return JsonResponse(data=data)
        except ObjectDoesNotExist:
            return HttpResponse("404")
    else:
        return HttpResponse("404")


@csrf_exempt
def getPeriodData(request):
    if request.method == "POST":
        retrieve_json_data = json.loads(request.body.decode('utf-8'))
        period = int(retrieve_json_data['period'])
        sensor_id = retrieve_json_data['id']
        data = {}

        try:
            iot_obj = IoT.objects.get(pk=sensor_id)
            readvalue = ReadValue.objects.filter(IoT_id=iot_obj).order_by('-datetime')[:period]
            array = []

            for rv in readvalue:
                msg = {}
                msg["value"] = rv.value
                msg["datetime"] = rv.datetime
                array.append(msg)

            data['read'] = array

            return JsonResponse(data=data)

        except ObjectDoesNotExist:
            return HttpResponse("404")

    else:
        return HttpResponse("404")


@csrf_exempt
def getLastIotData(request, iot_id):
    data = {}
    iot = IoT.objects.get(pk=iot_id)
    print(iot)
    readvalue = ReadValue.objects.filter(IoT_id=iot).order_by('-datetime')[:1]

    for rv in readvalue:
        data["value"] = rv.value
        data["type"] = rv.type
        data["datetime"] = rv.datetime

    return JsonResponse(data=data)


@csrf_exempt
def getLastData(request, type, iot_id):
    data = {}
    iot = IoT.objects.get(pk=iot_id)
    print(iot)
    readvalue = ReadValue.objects.filter(type=type, IoT_id=iot).order_by('-datetime')[:1]

    for rv in readvalue:
        data["value"] = rv.value
        data["type"] = rv.type
        data["datetime"] = rv.datetime

    return JsonResponse(data=data)


@csrf_exempt
def ds18b20(request):
    if request.method == "POST":
        retrieve_json_data = json.loads(request.body.decode('utf-8'))
        iot_pin = retrieve_json_data['pin']
        iot_key = retrieve_json_data['key']
        iot_value = retrieve_json_data['value']

        # return sensor id of sensor that has this pin and key content
        try:
            iot_id = IoT.objects.filter(pin=iot_pin, key=iot_key).get()
            ReadValue.objects.create(
                type="temperature",
                value=iot_value,
                datetime=datetime.datetime.now(),
                IoT_id=iot_id
            )
            return HttpResponse("200")
        except ObjectDoesNotExist:
            return HttpResponse("404")
    else:
        return HttpResponse("404")


@csrf_exempt
def store_sensor_data(request):
    if request.method == "POST":
        retrieve_json_data = json.loads(request.body.decode('utf-8'))
        iot_pin = retrieve_json_data['pin']
        iot_key = retrieve_json_data['key']
        iot_value = retrieve_json_data['value']
        iot_type = retrieve_json_data['type']

        # return sensor id of sensor that has this pin and key content
        try:
            iot_id = IoT.objects.filter(pin=iot_pin, key=iot_key).get()
            ReadValue.objects.create(
                type=iot_type,
                value=iot_value,
                datetime=datetime.datetime.now(),
                IoT_id=iot_id
            )
            return HttpResponse("200")
        except ObjectDoesNotExist:
            return HttpResponse("404")
    else:
        return HttpResponse("404")



@csrf_exempt
def clujbike(request):
    url = 'http://portal.clujbike.eu/Station/Read?Grid-sort=StationName-asc'
    json_response = {}
    json_station_array = []
    json_station = {}

    response = requests.post(url)
    json_data = json.loads(response.text)
    json_first_level = json_data['Data']

    for level in json_first_level:
        if (level['StationName'] == "G.Cosbuc"):
            json_station['name'] = 'G.Cosbuc'
            json_station['ocupate'] = level['OcuppiedSpots']
            json_station['libere'] = level['EmptySpots']
            json_station['status'] = level['Status']
            json_station_array.append(json_station)
            json_station={}
        elif (level['StationName'] == "Piata Mihai Viteazul"):
            json_station['name'] = 'Mihai.Viteazul'
            json_station['ocupate'] = level['OcuppiedSpots']
            json_station['libere'] = level['EmptySpots']
            json_station['status'] = level['Status']
            json_station_array.append(json_station)

    json_response['data'] = json_station_array
    print(json.dumps(json_response))

    return JsonResponse(data=json_response)

@csrf_exempt
def getRelayStatus(request):
    url = "http://192.168.1.10/getState"
    json_data = {}
    json_data["SECRET_KEY"] = "__secret_key_here__"
    response = requests.post(url, data = json.dumps(json_data))
    json_data = json.loads(response.text)
    print(json_data)

    return JsonResponse(data=json_data)

@csrf_exempt
def setRelayStatus(request):
    url = "http://192.168.1.10/setState"
    retrieve_json_data = json.loads(request.body.decode('utf-8'))
    json_request = {}
    json_request["SECRET_KEY"] = "__secret_key_here__"
    print(retrieve_json_data)
    json_request["Relay"] = retrieve_json_data["Relay"]
    json_request["State"] = retrieve_json_data["Status"]
    print(json.dumps(json_request))
    response = requests.post(url, data = json.dumps(json_request))
    json_data = json.loads(response.text)
    print(json_data)

    return JsonResponse(data=json_data)

@csrf_exempt
def resetRelays(request):
    url = "http://192.168.1.10/reset"
    json_data = "{\"SECRET_KEY\": \"__secret_key_here__\"}"
    response = requests.post(url, data =json_data)
    json_data = json.loads(response.text)
    print(json_data)

    return JsonResponse(data=json_data)
