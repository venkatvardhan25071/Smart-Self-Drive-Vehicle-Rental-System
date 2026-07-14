from django.db import models

class HostVehicle(models.Model):
    VEHICLE_TYPES = [
        ('Car', 'Car'),
        ('Bike', 'Bike'),
    ]

    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPES)
    brand = models.CharField(max_length=100)
    model_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100, unique=True)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_photo = models.ImageField(upload_to='host_vehicles/', null=True, blank=True)
    
    # Contact info
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    owner_phone = models.CharField(max_length=20, null=True, blank=True)
    
    status = models.CharField(max_length=50, default='Pending Review')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.registration_number})"

    class Meta:
        verbose_name = "Hosted Vehicle"
        verbose_name_plural = "Hosted Vehicles"
