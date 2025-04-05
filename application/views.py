
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import CategoryEntry,VehicleEntry
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CategoryEntryForm
from django.db.models import Q, Count
from django.contrib.auth import authenticate, logout,login
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required




@never_cache
@login_required(login_url="login")
def category_entry(request):
    search_query = request.GET.get('query')
    if search_query:
        multi_search = Q(vehicle_type__icontains=search_query)|Q(parking_area_no__icontains=search_query)|Q(vehicle_limit__icontains=search_query)|Q(parking_charge__icontains=search_query)
        category_data = CategoryEntry.objects.filter(multi_search)
    else:
        category_data = CategoryEntry.objects.all()

    if request.method == 'POST':
        parking = request.POST['parking']
        type = request.POST['type']
        limit = request.POST['limit']
        charge = request.POST['charge']

        create = CategoryEntry(parking_area_no=parking,vehicle_type= type,vehicle_limit=limit,parking_charge=charge)
        create.save()
        return redirect('category_entry')

    page_number = request.GET.get('page')
    paginator = Paginator(category_data, 5)
    try:
        category_data = paginator.page(page_number)
    except PageNotAnInteger:
        category_data = paginator.page(1)
    except EmptyPage:
        category_data = paginator.page(paginator.num_pages)

    context = {'category_data':category_data}
    return render(request, 'addCategory.html', context)

@never_cache
@login_required(login_url="login")
def deactivate_category(request,id):
    Category = CategoryEntry.objects.get(id=id)
    Category.status= "deactivated"
    Category.save()
    category_data =CategoryEntry.objects.all()
    context ={'category_data': category_data}
    return render(request,'addCategory.html',context)


@never_cache
@login_required(login_url="login")
def activate_category(request,id):
    Category = CategoryEntry.objects.get(id=id)
    Category.status = 'activated'
    Category.save()
    category_data = CategoryEntry.objects.all()
    context ={ 'category_data': category_data}
    return render(request, 'addCategory.html', context)

@never_cache
@login_required(login_url="login")
def delete_category(request,id):
    Category = CategoryEntry.objects.get(id=id)
    Category.delete()
    return redirect('category_entry')


@never_cache
@login_required(login_url="login")
def vehicle_entry(request):
    vehicle_type = CategoryEntry.objects.values_list('vehicle_type', flat=True).distinct()
    parking_charge = CategoryEntry.objects.values_list('parking_charge', flat=True).distinct()
    vehicle_counts = VehicleEntry.objects.values('vehicle_type').annotate(vehicle_count=Count('id'))
    data = []
    for x in CategoryEntry.objects.all():
        type = x.vehicle_type
        limit = x.vehicle_limit
        count = next((item['vehicle_count'] for item in vehicle_counts if item['vehicle_type'] == type), 0)
        limit = int(limit)
        count = int(count)
        counts = limit - count
        data.append({'vehicle_type': type, "vehicle_limit": limit, 'counts': counts})

    search_query = request.GET.get('query')
    if search_query:
        multi_search = Q(vehicle_type__icontains=search_query) | Q(
            vehicle_limit__icontains=search_query) | Q(parking_charge__icontains=search_query)
        vehicle = VehicleEntry.objects.filter(multi_search)
    else:
        vehicle = VehicleEntry.objects.all()

    if request.method == 'POST':
        vehicle_no = request.POST.get('vehicle_no')
        type = request.POST.get('type')
        parking_area_no_id = request.POST.get('parking_area_no')  # Now this is the id
        charge = request.POST.get('charge')
        try:
            author = CategoryEntry.objects.get(pk=parking_area_no_id)  # Use pk instead
            VehicleEntry.objects.create(vehicle_no=vehicle_no, vehicle_type=type, parking_area_no=author, parking_charge=charge)
            messages.success(request, "Vehicle entry recorded successfully.")
            return redirect('vehicle_entry')
        except CategoryEntry.DoesNotExist:
            messages.error(request, "Invalid parking area selected.")
        except CategoryEntry.MultipleObjectsReturned:
            messages.error(request, "Multiple parking areas found; please contact support.")

    page_num = request.GET.get('page')
    paginator = Paginator(vehicle, 4)
    try:
        vehicle = paginator.page(page_num)
    except PageNotAnInteger:
        vehicle = paginator.page(1)
    except EmptyPage:
        vehicle = paginator.page(paginator.num_pages)

    category_data = CategoryEntry.objects.all()  # Updated to pass full objects
    count = CategoryEntry.objects.all()
    context = {
        'vehicle_type': vehicle_type,
        'parking_charge': parking_charge,
        'vehicle': vehicle,
        'category_data': category_data,
        'count': count,
        'data': data
    }
    return render(request, 'vehicleEntry.html', context)




@never_cache
@login_required(login_url="login")
def manage_vehicles(request):
    search_query =request.GET.get('search')
    if search_query == None:
        vehicles = VehicleEntry.objects.all()
    else:

        vehicles = VehicleEntry.objects.filter(vehicle_type__icontains=search_query)

    page_num = request.GET.get('page')
    paginator = Paginator(vehicles,2)

    try:
        vehicles = paginator.page(page_num)
    except PageNotAnInteger:
        vehicles = paginator.page(1)
    except EmptyPage:
        vehicles = paginator.page(paginator.num_pages)

    context = {'vehicles': vehicles}
    return render(request, 'manageVehicles.html',context)


@never_cache
@login_required(login_url="login")
def change_status_vehicle_entry(request, id):
    vehicle_entry= VehicleEntry.objects.get(id=id)
    if vehicle_entry.status == 'parked':
        vehicle_entry.status = 'leaved'
    else:
        vehicle_entry.status ='parked'
    vehicle_entry.save()
    return redirect('manage_vehicles')



@never_cache
@login_required(login_url="login")
def search(request):
    search_query = request.GET.get('search')
    if search_query is None:
        vehicles = VehicleEntry.objects.all()
    else:
        multi_search=Q(vehicle_type__icontains=search_query)|Q(vehicle_no__icontains=search_query)|Q(parking_charge__icontains=search_query)
        vehicles = VehicleEntry.objects.filter(multi_search)
    context = {'vehicles': vehicles}
    return render(request, 'search.html', context)


@never_cache
@login_required(login_url="login")
def base(request):
    superuser = User.objects.filter(is_superuser=True).first()
    superuser_username = superuser.username if superuser else None

    return render(request,'base.html',{'user': superuser_username})


@never_cache
@login_required(login_url="login")
def accountSetting(request):
    if request.method == 'POST':
        current_pass = request.POST.get('current')
        new_pass = request.POST.get('n_pass1')
        re_pass = request.POST.get('n_pass2')

        if not request.user.check_password(current_pass):
            messages.error(request, 'Current password is not correct')
            return redirect('accountSetting')
        if new_pass != re_pass:
            messages.error(
                request, 'New password and re-entered password do not match')
            return redirect('accountSetting')

        if new_pass == current_pass:
            messages.error(
                request, 'New password cannot be same as current password do not match')
            return redirect('accountSetting')
        request.user.set_password(new_pass)
        request.user.save()
        login(request, request.user)
        messages.success(request, 'Password changed Successfully')
        return render(request, 'accountSetting.html')
    return render(request, 'accountSetting.html')





def login_view(request):
    if request.method == "POST":
        users = request.POST.get('user')
        password = request.POST.get('pass')

        user = authenticate(request, username=users, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'login.html')

def logouts (request):
    logout(request)
    return render(request, 'login.html')

@never_cache
@login_required(login_url="login")
def dashboard(request):
    vehicles_parked = VehicleEntry.objects.filter(status='parked').count()
    vehicles_departed = VehicleEntry.objects.filter(status='leaved').count()
    available_category = CategoryEntry.objects.all().count()
    earnings = VehicleEntry.objects.values_list('parking_charge', flat=True).filter(status='leaved')
    print(earnings)
    temp =0
    for i in earnings:
        temp =temp+float(i)
    tot_earnings =int(temp)

    tot_records = VehicleEntry.objects.all().count()
    vehicle_limits = CategoryEntry.objects.values_list('vehicle_limit',flat=True)
    tot_vehicle_limit = sum(int(limit) for limit in vehicle_limits if limit.isdigit())

    context ={'parked': vehicles_parked, 'departed':vehicles_departed,'tot_category' :available_category,
              'tot_earnings':tot_earnings, 'tot_records':tot_records,'tot_vehicle_limit':tot_vehicle_limit}

    return render(request,'dashBoard.html',context)

@never_cache
@login_required(login_url="login")
def edit(request):
    if request.method == 'POST':
     category = CategoryEntry.objects.get(id=request.POST.get('id'))
     category.parking_area_no = request.POST.get('parkingAreaNumber')
     category.vehicle_type = request.POST.get('vehicleType')
     category.vehicle_limit = request.POST.get('vehicleLimit')
     category.parking_charge = request.POST.get('parkingCharge')
     category.save()
     return redirect('category_entry')

