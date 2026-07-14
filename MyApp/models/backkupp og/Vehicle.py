from django.db import models
from .category import Category


class Vehicle(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='' , null=True , blank=True)
    image = models.ImageField(upload_to='uploads/products/')
    car_id = models.IntegerField(default=0)

    @staticmethod
    def get_vehicles_by_id(ids):
        return Vehicle.objects.filter(id__in =ids)

    @staticmethod
    def get_all_vehicles():
        return Vehicle.objects.all()

    @staticmethod
    def get_all_vehicles_by_categoryid(category_id):
        if category_id:
            return Vehicle.objects.filter(category = category_id)
        else:
            return Vehicle.get_all_vehicles();