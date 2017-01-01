from django.contrib import admin
from .models import IoT, CommunicationModel, ReadValue


admin.site.register(IoT)
admin.site.register(CommunicationModel)
admin.site.register(ReadValue)
