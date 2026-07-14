from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    re_enter_password = models.CharField(max_length=255, null=True, blank=True, default="")


    def __str__(self):
        # safe fallback if fields are empty
        return f"{self.name or 'No name'} {self.username or 'No username'}"

    def register(self):
        """
        A simple wrapper to save this model.
        You can call customer.register() from views if you want.
        """
        self.save()
        
        
        
        
        
        
        
        


        
   