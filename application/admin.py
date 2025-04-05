from django.contrib import admin
from .models import CategoryEntry,VehicleEntry
class ParkingAreaAdmin(admin.ModelAdmin):
    list_display = ('parking_area_no', 'vehicle_type', 'vehicle_limit', 'parking_charge', 'status', 'doc')
admin.site.register(CategoryEntry,ParkingAreaAdmin)

class ParkingAreaAdmin1(admin.ModelAdmin):
    list_display = ('vehicle_no','parking_area_no','vehicle_type' ,'parking_charge','status','arrival_time')
admin.site.register(VehicleEntry,ParkingAreaAdmin1)