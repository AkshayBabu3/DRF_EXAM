from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CarDb(models.Model):

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    reg_no = models.CharField(max_length=20,unique=True)
    rent_per_day = models.DecimalField(max_digits=8,decimal_places=2)
    fuel_type = models.CharField(max_length=20)
    is_avilable = models.BooleanField(default=True)
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.brand

class RentalDb(models.Model):
    car = models.ForeignKey(CarDb,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} - {self.car.brand}"