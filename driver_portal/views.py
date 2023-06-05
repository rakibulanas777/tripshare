from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from driver_portal.models import *
from customer_portal.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'driver_portal/login.html')
    else:
        return render(request, 'driver_portal/home_page.html')

def login(request):
    return render(request, 'driver_portal/login.html')


def auth_view(request):
    if request.user.is_authenticated:
        return render(request, 'driver_portal/home_page.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        try:
            driver_portal = CarDriver.objects.get(driver_portal = user)
        except:
            driver_portal = None
        if driver_portal is not None:
            auth.login(request, user)
            return render(request, 'driver_portal/home_page.html')
        else:
            return render(request, 'driver_portal/login_failed.html')

def logout_view(request):
    auth.logout(request)
    return render(request, 'driver_portal/login.html')

def register(request):
    return render(request, 'driver_portal/register.html')

def registration(request):
    username = request.POST['username']
    password = request.POST['password']
    mobile = request.POST['mobile']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']

    try:
        user = User.objects.create_user(username = username, password = password, email = email)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
    except:
        return render(request, 'driver_portal/registration_error.html')
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        driver_portal = CarDriver(driver_portal = user, mobile = mobile, area=area)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        driver_portal = CarDriver(driver_portal = user, mobile = mobile, area=area)
    driver_portal.save()
    return render(request, 'driver_portal/registered.html')

@login_required
def add_vehicle(request):
    car_name = request.POST['car_name']
    color = request.POST['color']
    cd = CarDriver.objects.get(driver_portal=request.user)
    city = request.POST['city']
    city = city.lower()
    pincode = request.POST['pincode']
    description = request.POST['description']
    capacity = request.POST['capacity']
    try:
        area = Area.objects.get(city = city, pincode = pincode)
    except:
        area = None
    if area is not None:
        car = Vehicles(car_name=car_name, color=color, dealer=cd, area = area, description = description, capacity=capacity)
    else:
        area = Area(city = city, pincode = pincode)
        area.save()
        area = Area.objects.get(city = city, pincode = pincode)
        car = Vehicles(car_name=car_name, color=color, dealer=cd, area = area,description=description, capacity=capacity)
    car.save()
    return render(request, 'driver_portal/vehicle_added.html')

@login_required
def manage_vehicles(request):
    username = request.user
    user = User.objects.get(username = username)
    driver_portal = CarDriver.objects.get(driver_portal = user)
    vehicle_list = []
    vehicles = Vehicles.objects.filter(dealer = driver_portal)
    for v in vehicles:
        vehicle_list.append(v)
    return render(request, 'driver_portal/manage.html', {'vehicle_list':vehicle_list})

@login_required
def order_list(request):
    username = request.user
    user = User.objects.get(username = username)
    driver_portal = CarDriver.objects.get(driver_portal = user)
    orders = Orders.objects.filter(driver_portal = driver_portal)
    order_list = []
    for o in orders:
        if o.is_complete == False:
            order_list.append(o)
    return render(request, 'driver_portal/order_list.html', {'order_list':order_list})

@login_required
def complete(request):
    order_id = request.POST['id']
    order = Orders.objects.get(id = order_id)
    vehicle = order.vehicle
    order.is_complete = True
    order.save()
    vehicle.is_available = True
    vehicle.save()
    return HttpResponseRedirect('/driver_portal/order_list/')


@login_required
def history(request):
    user = User.objects.get(username = request.user)
    driver_portal = CarDriver.objects.get(driver_portal = user)
    orders = Orders.objects.filter(driver_portal = driver_portal)
    order_list = []
    for o in orders:
        order_list.append(o)
    return render(request, 'driver_portal/history.html', {'wallet':driver_portal.wallet, 'order_list':order_list})

@login_required
def delete(request):
    veh_id = request.POST['id']
    vehicle = Vehicles.objects.get(id = veh_id)
    vehicle.delete()
    return HttpResponseRedirect('/driver_portal/manage_vehicles/')
