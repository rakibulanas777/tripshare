from django.urls import path,include, re_path
# from django.conf.urls import url
from home.views import *
from car_dealer_portal import *
from customer_portal import *

urlpatterns = [
    re_path(r'^$',home_page),
    re_path(r'^team/',team_page),
    re_path(r'^contact/',contact_page),
]
