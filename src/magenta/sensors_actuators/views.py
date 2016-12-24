from django.shortcuts import render
from django.http import HttpResponse


def sensors(request):
    return HttpResponse("hey there you are on the sensors page")


def actuators(request):
    return HttpResponse("Hey there you are on the actuators page")


def dashboard(request):
    return HttpResponse("Hey there you are on the dashboard page")