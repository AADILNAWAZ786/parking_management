
from django.db import models
from datetime import datetime

class CategoryEntry(models.Model):
    PARKING_STATUS_CHOICES = [
        ('activated', 'Activated'),
        ('deactivated', 'Deactivated'),
    ]

    parking_area_no = models.CharField(max_length=100, blank=False, null=False)
    vehicle_type = models.CharField(max_length=100, blank=False, null=False)
    vehicle_limit = models.CharField(max_length=200, blank=False, null=False)
    parking_charge = models.CharField(max_length=200, blank=False, null=False)
    status = models.CharField(max_length=100, choices=PARKING_STATUS_CHOICES, default='activated')
    doc = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.parking_area_no

class VehicleEntry(models.Model):
    VEHICLE_STATUS_CHOICES =[
        ('parked','parked'),
        ('leaved','leaved')
    ]
    vehicle_no = models.CharField(max_length=11, null=False, blank=False)
    parking_area_no = models.ForeignKey(CategoryEntry, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=30, blank=False, null=False)
    parking_charge = models.CharField(max_length=10, blank=False, null=False)
    status = models.CharField(max_length=20, choices=VEHICLE_STATUS_CHOICES, default='parked')
    arrival_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.vehicle_no


