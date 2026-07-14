from django.db import models
from .vehicle import Vehicle  # or wherever your main Vehicle model is

class LuxuryVehicle(Vehicle):
    class Meta:
        proxy = True
        verbose_name = "Luxury Vehicle"
        verbose_name_plural = "Luxury Vehicles"

class Bike(Vehicle):
    class Meta:
        proxy = True
        verbose_name = "Bike"
        verbose_name_plural = "Bikes"

class Scooter(Vehicle):
    class Meta:
        proxy = True
        verbose_name = "Scooter"
        verbose_name_plural = "Scooters"
