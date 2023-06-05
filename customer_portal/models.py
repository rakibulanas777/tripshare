from django.db import models
from django.db import models
from django.core.validators import *
from django.contrib.auth.models import User
from driver_portal.models import *
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(validators = [MinLengthValidator(10), MaxLengthValidator(13)], max_length = 13)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    driver_portal = models.ForeignKey(CarDriver, on_delete=models.PROTECT)
    rent = models.CharField(max_length=8)
    vehicle = models.ForeignKey(Vehicles, on_delete=models.PROTECT)
    start_destination = models.CharField(max_length = 30)
    final_destination = models.CharField(max_length = 30)
    distance = models.CharField(max_length = 3)
    is_complete = models.BooleanField(default = False)
