from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime
from django.conf import settings
import os
import json
import datetime
import requests
import logging

from .models import ReadValue, IoT

logger = logging.getLogger(__name__)
TEMPERATURE_TYPE = "temperature"


def handler404(request):
    logger.error ("404 generated for request:{0}".format(request))
    return render(request, "404.html", status=404)


def sensors(request):
    logger.debug("In sensors with request: {0}".format(request))
    context = {}
    context['iot_objects'] = ReadValue.objects.filter(type=TEMPERATURE_TYPE).order_by('-datetime')[:20]
    context["title"] = "Sensor"
    logger.debug("Send response for sensor type={0}, with context: {1}".format(type,context))

    return render(request=request,
                  context=context,
                  template_name="sensors_actuators/index.html")


def actuators(request):
    logger.debug("In actuators with request: {0}".format(request))
    return render(request=request,
                  template_name="sensors_actuators/actuators.html")


def dashboard(request):
    logger.debug("In dashboard with request: {0}".format(request))
    context = {}
    logger.debug("Dashboard response: {0}".format(context))

    return render(request=request,
                  context=context,
                  template_name="sensors_actuators/dashboard.html")


@csrf_exempt
def getIots(request):
    logger.debug("In getIots: request:{0}".format(request))
    response_json = {}
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
            response_json['iot'] = array
            
            logger.debug("In getIots: JSON response ready with value:{0}".format(response_json))

            return JsonResponse(data=response_json)
        except ObjectDoesNotExist as oe:
            logger.warning("In getIots: ObjectDoesNotExist exception raised: {0}".format(oe))

            return HttpResponse("404")
        except Exception as ex:
            logger.error("In getIots: Exception raised: {0}".format(ex))

            return HttpResponse("404")
    else:
        logger.error("In getIots: wrong request method: {0}".format(request.method))

        return HttpResponse("404")


@csrf_exempt
def getIotReadingErrors(request):
    logger.debug("In getIotReadingErrors: request:{0}".format(request))
    response_json ={}
    iot_array = []
    if request.method == "POST":
        iot_objects = IoT.objects.filter(status="active").order_by("id")
        try:
            for iot in iot_objects:
                readvalue = ReadValue.objects.filter(IoT_id=iot).order_by('-datetime')[:1]
                
                for rv in readvalue:
                    oneHourLater = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)
                    if (rv.datetime < oneHourLater):
                        iot_array.append(iot.name)
            response_json['response'] = iot_array                   
            logger.debug("In getIotReadingErrors: JSON response ready with value:{0}".format(response_json))
            
            return JsonResponse(data=response_json)
        except ObjectDoesNotExistas as oe:
            logger.warning("In getIotReadingErrors: ObjectDoesNotExist exception raised: {0}".format(oe))

            return HttpResponse("404")
        except Exception as ex:
            logger.error("In getIotReadingErrors: Exception raised: {0}".format(ex))

            return HttpResponse("404")
    else:
        logger.error("In getIotReadingErrors: wrong request method:{0}".format(request.method))

        return HttpResponse("404")

@csrf_exempt
def getSensorDataForInterval(request):
    response_json = {}
    array = []
    logger.debug("In getSensorDataForInterval: request:{0}".format(request))
        
    if request.method == "POST":
        retrieve_json_data = json.loads(request.body.decode('utf-8'))
        
        requestStartDate = datetime.datetime.strptime(retrieve_json_data['startPeriod'], "%Y-%m-%d %H:%M")
        requestEndDate = datetime.datetime.strptime(retrieve_json_data['endPeriod'], "%Y-%m-%d %H:%M")
        iot_id = retrieve_json_data['id']
        
        try:
            iot_object = IoT.objects.get(pk=iot_id)
            readvalue = ReadValue.objects.filter(IoT_id=iot_object, datetime__range=(requestStartDate, requestEndDate)).order_by('datetime')
            
            for rv in readvalue:
                msg = {}
                msg['datetime'] = rv.datetime.strftime('%Y-%m-%d %H:%M')
                msg['value'] = rv.value
                array.append(msg)
            
            response_json['id'] = iot_object.id
            response_json['name'] = iot_object.name
            response_json['results'] = array
            logger.debug("In getSensorDataForInterval: JSON response ready with value:{0}".format(response_json))

            return JsonResponse(data=response_json)
        except ObjectDoesNotExist as oe:
            logger.warning("In getSensorDataForInterval: ObjectDoesNotExist exception raised: {0}".format(oe))
            
            return HttpResponse("404")
        except IndexError as ie:
            logger.warning("In getSensorDataForInterval: IndexError exception raised: {0}".format(ie))
            
            return HttpResponse("404")
        except Exception as e:
            logger.error("In getSensorDataForInterval: Exception raised: {0}".format(e))
            
            return HttpResponse("404")
    else:
        logger.error("In getSensorDataForInterval: wrong request method exception: {0}".format(request.method))
            
        return HttpResponse("404")


@csrf_exempt
def getPeriodData(request):
    logger.debug("In getPeriodData: request:{0}".format(request))
    
    if request.method == "POST":
        retrieve_json_data = json.loads(request.body.decode('utf-8'))
        period = int(retrieve_json_data['period'])
        sensor_id = retrieve_json_data['id']
        response_json = {}

        try:
            iot_obj = IoT.objects.get(pk=sensor_id)
            readvalue = ReadValue.objects.filter(IoT_id=iot_obj).order_by('-datetime')[:period]
            array = []
            for rv in readvalue:
                msg = {}
                msg["value"] = rv.value
                msg["datetime"] = rv.datetime
                array.append(msg)
            response_json['read'] = array
            logger.debug("In getPeriodData: JSON response ready with value:{0}".format(response_json))

            return JsonResponse(data=response_json)
        except ObjectDoesNotExist as oe:
            logger.warning("In getPeriodData: ObjectDoesNotExist exception raised: {0}".format(oe))
            
            return HttpResponse("404")
        except Exception as e:
            logger.error("In getPeriodData: Exception raised: {0}".format(e))
            
            return HttpResponse("404")
    else:
        logger.error("In getPeriodData: Wrong request method: {0}".format(request.method))

        return HttpResponse("404")


@csrf_exempt
def getLastIotData(request, iot_id):
    logger.debug("In getLastIotData: request:{0} and iot_id {1}".format(request, iot_id))
    
    response_json = {}
    try: 
        iot = IoT.objects.get(pk=iot_id)
        readvalue = ReadValue.objects.filter(IoT_id=iot).order_by('-datetime')[:1]

        for rv in readvalue:
            response_json["value"] = rv.value
            response_json["type"] = rv.type
            response_json["datetime"] = rv.datetime
    except Exception as ex:
            logger.error("In getLastIotData: Exception raised: {0}".format(ex))

            return HttpResponse("404")
    
    logger.debug("In getLastIotData: Response ready with message:{0}".format(response_json))
    return JsonResponse(data=response_json)


@csrf_exempt
def getLastData(request, type_value, iot_id):
    logger.debug("In getLastData: request:{0}, type:{1} and iot_id: {2}".format(request, type_value, iot_id))
    
    response_json = {}
    try:
        iot = IoT.objects.get(pk=iot_id)
        readvalue = ReadValue.objects.filter(type=type_value, IoT_id=iot).order_by('-datetime')[:1]

        for rv in readvalue:
            response_json["value"] = rv.value
            response_json["type"] = rv.type
            response_json["datetime"] = rv.datetime
    except Exception as ex:
        logger.error("In getLastIotData: Exception raised: {0}".format(ex))

        return HttpResponse("404")

    logger.debug("In getLastData: Response ready with message:{0}".format(response_json))
    return JsonResponse(data=response_json)


@csrf_exempt
def ds18b20(request):
    logger.debug("In ds18b20: request:{0}".format(request))
    
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
            logger.debug("In ds18b20: New record created, for JSON :{0}".format(retrieve_json_data))
            
            return HttpResponse("200")
        except ObjectDoesNotExist as oe:
            logger.warning("In ds18b20: ObjectDoesNotExist raised: {0} for JSON: {1}".format(oe, retrieve_json_data))

            return HttpResponse("404")
        except Exception as ex:
            logger.error("In ds18b20: Exception raised: {0} for JSON: {1}".format(ex, retrieve_json_data))

            return HttpResponse("404")
    else:
        logger.error("In ds18b20: wrong request method :{0}".format(request.method))
    
        return HttpResponse("404")


@csrf_exempt
def store_sensor_data(request):
    logger.debug("In store_sensor_data: request:{0}".format(request))
    
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
            logger.debug("In store_sensor_data: New record created, for JSON :{0}".format(retrieve_json_data))

            return HttpResponse("200")
        except ObjectDoesNotExist as oe:
            logger.warning("In store_sensor_data: ObjectDoesNotExist raised: {0} for JSON: {1}".format(oe, retrieve_json_data))

            return HttpResponse("404")
        except Exception as ex:
            logger.error("In store_sensor_data: Exception raised: {0} for JSON: {1}".format(ex, retrieve_json_data))

            return HttpResponse("404")
    else:
        logger.error("In store_sensor_data: wrong request method :{0}".format(request.method))
    
        return HttpResponse("404")


@csrf_exempt
def getRelayStatus(request):
    logger.debug("In getRelayStatus: request:{0}".format(request))

    url = "http://192.168.1.10/getState"
    json_data = {}
    json_data["SECRET_KEY"] = "__secret_key_here__"
    response = requests.post(url, data = json.dumps(json_data))
    json_data = json.loads(response.text)
    logger.debug("In getRelayStatus: resopnse ready:{0}".format(json_data))

    return JsonResponse(data=json_data)


@csrf_exempt
def setRelayStatus(request):
    logger.debug("In setRelayStatus: request:{0}".format(request))

    url = "http://192.168.1.10/setState"
    retrieve_json_data = json.loads(request.body.decode('utf-8'))
    json_request = {}
    json_request["SECRET_KEY"] = "__secret_key_here__"
    json_request["Relay"] = retrieve_json_data["Relay"]
    json_request["State"] = retrieve_json_data["Status"]
    response = requests.post(url, data = json.dumps(json_request))
    json_data = json.loads(response.text)
    logger.debug("In setRelayStatus: resopnse ready:{0}".format(json_data))

    return JsonResponse(data=json_data)


@csrf_exempt
def resetRelays(request):
    logger.debug("In resetRelays: request:{0}".format(request))
    
    url = "http://192.168.1.10/reset"
    json_data = "{\"SECRET_KEY\": \"__secret_key_here__\"}"
    response = requests.post(url, data =json_data)
    json_data = json.loads(response.text)
    logger.debug("In resetRelays: resopnse ready:{0}".format(json_data))
    
    return JsonResponse(data=json_data)


def scheduler(request):
    logger.debug("In scheduler with request: {0}".format(request))
    path = os.path.join(settings.BASE_DIR, "static/resources/json/scheduler.json")
    json_file = open(path).read()
    logger.debug("Sending Scheduler JSON: {0}".format(json_file))
    context = {}
    context["json"]=json_file
    return render(request=request,
                  context=context,
                  template_name="sensors_actuators/scheduler.html")


@csrf_exempt
def store_scheduler(request):
    logger.debug("In store_scheduler: request:{0} with content {1}".format(request, request.body.decode('utf-8')))
    if request.method == "POST":
        retrieve_json_data = json.loads(request.body.decode('utf-8'))
        path = os.path.join(settings.BASE_DIR, "static/resources/json/scheduler.json")
        logger.debug("write JSON message: {0} to path {1}.".format(retrieve_json_data, path))
        with open(path, 'w') as outfile:
            json.dump(retrieve_json_data, outfile)
    else:
        logger.error("Wrong request make. Expected POST.")

    return HttpResponse(status=200)