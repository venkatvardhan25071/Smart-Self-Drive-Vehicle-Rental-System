from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Personal & Contact Info
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField()

    # Vehicle & Trip Details (From Page 1)
    vehicle_name = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    pickup_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    
    # Financials
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Document Uploads (From Page 2)
    aadhaar_card = models.FileField(upload_to='documents/aadhaar/', null=True, blank=True)
    driving_license = models.FileField(upload_to='documents/dl/', null=True, blank=True)
    
    # Payment Details
    payment_method = models.CharField(max_length=50) # 'cards' or 'upi'
    card_number = models.CharField(max_length=12, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Stripe / Status
    stripe_checkout_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.vehicle_name} ({self.status})"

class CancellationRequest(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='cancellation')
    reason = models.CharField(max_length=255)
    issue = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending') # Pending, Accepted, Rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancellation Request for {self.booking.vehicle_name} ({self.status})"