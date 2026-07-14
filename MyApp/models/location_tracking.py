from django.db import models

from .vehicle import Vehicle


class RentalHub(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class VehicleAvailabilitySignal(models.Model):
    SIGNAL_CHOICES = [
        ("high", "High"),
        ("medium", "Medium"),
        ("low", "Low"),
        ("unavailable", "Unavailable"),
    ]

    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="availability_signals"
    )
    hub = models.ForeignKey(
        RentalHub, on_delete=models.CASCADE, related_name="availability_signals"
    )
    signal = models.CharField(max_length=20, choices=SIGNAL_CHOICES, default="high")
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("vehicle", "hub")
        ordering = ["hub__name", "vehicle__name"]

    def __str__(self):
        return f"{self.vehicle.name} @ {self.hub.name} ({self.signal})"

class ParkingLocation(models.Model):
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.city}"
