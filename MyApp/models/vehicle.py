from django.db import models
from .category import Category

class Vehicle(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default="", null=True, blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    car_id = models.IntegerField(default=0)
    
    @staticmethod
    def get_all_vehicles():
        return Vehicle.objects.all()

    @staticmethod
    def get_all_vehicles_by_categoryid(category_id):
        # if category_id is None or empty string, return all vehicles
        if not category_id:
            return Vehicle.get_all_vehicles()
        # use category_id lookup which accepts both int and string of int
        return Vehicle.objects.filter(category_id=category_id)
