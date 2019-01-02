from django.db import models


class IoT(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, auto_created=True)
    type = models.CharField(max_length=50, help_text="sensor/actuator")
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    status = models.CharField(max_length=100)
    pin = models.CharField(max_length=50)
    key = models.CharField(max_length=50)
    readInterval = models.IntegerField(help_text="seconds")

    def __str__(self):
        return str(self.id) + "|" + self.type + "|" + self.name + "|" + self.location


class CommunicationModel(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, auto_created=True)
    Method = models.CharField(max_length=50, help_text="Radio/HTTP/HTTPS/etc")
    Address = models.CharField(max_length=100, help_text="IP/Unique address for each action of the IoT device")
    URL = models.CharField(max_length=500)
    RequestType = models.CharField(max_length=100, help_text="GET/POST/etc")
    RequestModel = models.CharField(max_length=500, help_text="GET/POST model")
    IoT_id = models.ForeignKey('IoT', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.IoT_id) + "|" + self.Address


class ReadValue(models.Model):
    id = models.IntegerField(unique=True, primary_key=True, auto_created=True)
    type = models.CharField(max_length=100, help_text="temperature, pressure, humidity,etc")
    value = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    IoT_id = models.ForeignKey('IoT', on_delete=models.PROTECT)

    def __str__(self):
        return str(self.IoT_id) + "|" + self.type + "|" + str(self.datetime)

