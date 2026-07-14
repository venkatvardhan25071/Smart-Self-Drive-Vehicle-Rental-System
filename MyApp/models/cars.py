from email.policy import default
from django.db import models
from .category import Category
class Car(models.Model):
    
    car_id = models.IntegerField(default=0)
    car_name = models.CharField(max_length=30,default="")
    car_desc = models.CharField(max_length=300,default="",null=True,blank=True)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category ,on_delete=models.CASCADE , default=1)
    image = models.ImageField(upload_to="car/images",default="")

    def __str__(self):
        return self.car_name
    
    

    


    @staticmethod
    def get_all_cars():
        return Car.objects.all()

    @staticmethod
    def get_all_cars_by_categoryid(category_id):
        if category_id:
          return Car.objects.filter(category=category_id)
        else:
            return Car.get_all_cars();



    
    
    
    
    
    
    
    
    
    
    

        