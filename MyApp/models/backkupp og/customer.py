from django.db import models
from django.contrib.auth.models import User
class Customer(models.Model):
 username = models.CharField(max_length=100)
 email = models.EmailField()
 password = models.CharField()
 re_enter_password = models.CharField(max_length=255, default="")
      
    
    
    
def register(self):
    self.save()
        
def __str__(self):
    return self.username

 


 


 
#phone = models.CharField(max_length=11)
#first_name = models.CharField(max_length=100)
