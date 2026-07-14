from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    license_number = models.CharField(max_length=50, blank=True, null=True, default="")
    phone = models.CharField(max_length=20, blank=True, null=True, default="")
    address = models.CharField(max_length=255, blank=True, null=True, default="")
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True, default="")
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True, default="")
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
