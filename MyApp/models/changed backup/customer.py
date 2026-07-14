from django.db import models
from django.contrib.auth.models import User
class Customer(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField()
    password = models.CharField()
    re_enter_password = models.CharField(max_length=255, default="")
    def __str__(self):
        return f"{self.name} ({self.username})" 

 
   


    
    
    def User(self):
        self.save()
        
   