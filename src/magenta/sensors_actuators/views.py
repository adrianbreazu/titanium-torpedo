from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
import json
import datetime
from .models import ReadValue, IoT


def sensors(request):
    try:

        return HttpResponse("hey there you are on the sensors page")
    except Exception as e:
        print("error on dashboard: {0}".format(e))
    finally:
        print("done with dashboard")


def actuators(request):
    return HttpResponse("Hey there you are on the actuators page")



def dashboard(request):
    return render(request=request,
                  template_name="sensors_actuators/index.html")


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
            return HttpResponse("OK")
        except ObjectDoesNotExist:
            return HttpResponse("Not OK")
    else:
        return HttpResponse("Not OK")
