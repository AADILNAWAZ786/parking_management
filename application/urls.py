from django.urls import path
from django.contrib import admin
from . import views
from .views import category_entry

urlpatterns = [
    path('',views.login_view, name='login'),
    path('category_entry/',category_entry, name="category_entry"),
    path('dashboard',views.dashboard, name="dashboard"),
    path('vehicle_entry/',views.vehicle_entry,name='vehicle_entry'),
    path('manage_vehicles',views.manage_vehicles, name="manage_vehicles"),
    path('search',views.search,name='search'),
    path('accountSetting',views.accountSetting,name='accountSetting'),
    path('deactivate_category/<int:id>/',views.deactivate_category,name='deactivate_category'),
    path('activate_category/<int:id>/',views.activate_category,name='activate_category'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),
    path('base',views.base,name='user'),
    path('action/<int:id>/',views.change_status_vehicle_entry,name='action'),
    path('search',views.search,name='search'),
    path('logout',views.logouts,name='logout'),
    path('edit',views.edit, name='edit')

]