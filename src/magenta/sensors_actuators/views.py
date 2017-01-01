from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ReadValue, IoT
import datetime


def sensors(request):
    return HttpResponse("hey there you are on the sensors page")


def actuators(request):
    return HttpResponse("Hey there you are on the actuators page")


def dashboard(request):
    return render(request=request,
                  template_name="sensors_actuators/index.html")


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
