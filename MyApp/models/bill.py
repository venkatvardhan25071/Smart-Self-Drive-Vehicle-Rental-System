from django.db import models
from django.contrib.auth.models import User

class CarBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Customer Details
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)

    # Rental Details
    car_chosen = models.CharField(max_length=50)
    car_color = models.CharField(max_length=50)
    num_days = models.IntegerField()
    pickup_date = models.DateField()
    from_location = models.CharField(max_length=100)
    to_location = models.CharField(max_length=100)
    
    # Financials
    total_rent = models.DecimalField(max_digits=10, decimal_places=2)

    # Auto-populated fields
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Car Booking"
        verbose_name_plural = "Car Bookings"

    def __str__(self):
        return f"{self.full_name} - {self.car_chosen} on {self.pickup_date}"