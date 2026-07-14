from django.contrib import admin

from .models import customer
from .models.vehicle import Vehicle

from .models.category import Category
from .models.orders import Order
from .models.customer import Customer

from .models import Booking 
from .models.Booking import CancellationRequest

from .models import SupportTicket, HostVehicle


from django.utils.html import format_html


# This line is where the error triggers





from .models.proxy_models import LuxuryVehicle, Bike, Scooter

from .models import CarBooking
from .models import RentalHub, VehicleAvailabilitySignal









class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    
    

class VehiclesAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('id',)


@admin.register(LuxuryVehicle)
class LuxuryVehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(category__name__iexact="Luxury")


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(category__name__iexact="bike")


@admin.register(Scooter)
class ScooterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(category__name__iexact="scoty")



    



# Register your models here.
admin.site.register(Vehicle, VehiclesAdmin)  # 

admin.site.register(Category, CategoryAdmin)

admin.site.register(Order)
admin.site.register(Customer)











from django.urls import path
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Organize how data appears in the list view
    list_display = ('full_name', 'vehicle_name', 'location', 'total_amount', 'status', 'created_at', 'admin_actions')
    list_filter = ('status', 'location', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'vehicle_name')
    actions = ['accept_bookings', 'reject_bookings']

    @admin.action(description='Accept selected bookings')
    def accept_bookings(self, request, queryset):
        queryset.update(status='Accepted')

    @admin.action(description='Reject selected bookings')
    def reject_bookings(self, request, queryset):
        queryset.update(status='Rejected')

    @admin.action(description='Set selected bookings to Pending')
    def pending_bookings(self, request, queryset):
        queryset.update(status='Pending')
        
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:booking_id>/accept/', self.admin_site.admin_view(self.accept_booking_view), name='booking-accept'),
            path('<int:booking_id>/reject/', self.admin_site.admin_view(self.reject_booking_view), name='booking-reject'),
            path('<int:booking_id>/pending/', self.admin_site.admin_view(self.pending_booking_view), name='booking-pending'),
        ]
        return custom_urls + urls

    def accept_booking_view(self, request, booking_id):
        Booking.objects.filter(id=booking_id).update(status='Accepted')
        return redirect(request.META.get('HTTP_REFERER', 'admin:MyApp_booking_changelist'))

    def reject_booking_view(self, request, booking_id):
        Booking.objects.filter(id=booking_id).update(status='Rejected')
        return redirect(request.META.get('HTTP_REFERER', 'admin:MyApp_booking_changelist'))

    def pending_booking_view(self, request, booking_id):
        Booking.objects.filter(id=booking_id).update(status='Pending')
        return redirect(request.META.get('HTTP_REFERER', 'admin:MyApp_booking_changelist'))
        
    def admin_actions(self, obj):
        return format_html(
            '<a class="button" style="background:linear-gradient(135deg, #10b981, #059669) !important; box-shadow:0 3px 10px rgba(5,150,105,.3) !important; color:#ffffff !important; margin-right:5px; padding:6px 12px; border:none !important;" href="{}">Accept</a>'
            '<a class="button" style="background:linear-gradient(135deg, #f59e0b, #d97706) !important; box-shadow:0 3px 10px rgba(245,158,11,.3) !important; color:#ffffff !important; margin-right:5px; padding:6px 12px; border:none !important;" href="{}">Pending</a>'
            '<a class="button" style="background:linear-gradient(135deg, #ef4444, #dc2626) !important; box-shadow:0 3px 10px rgba(239,68,68,.3) !important; color:#ffffff !important; padding:6px 12px; border:none !important;" href="{}">Reject</a>',
            reverse('admin:booking-accept', args=[obj.id]),
            reverse('admin:booking-pending', args=[obj.id]),
            reverse('admin:booking-reject', args=[obj.id]),
        )
    admin_actions.short_description = 'Actions'
    
    # Organize the detail view into sections
    fieldsets = (
        ('Customer Info', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('vehicle_name', 'color', 'location', 'pickup_date', 'return_date', 'total_amount')
        }),
        ('Documents', {
            'fields': ('aadhaar_card', 'driving_license')
        }),
        ('Payment Info', {
            'fields': ('payment_method', 'card_number', 'upi_id', 'stripe_checkout_id', 'status')
        }),
    )
    readonly_fields = ('stripe_checkout_id', 'created_at')


@admin.register(RentalHub)
class RentalHubAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(VehicleAvailabilitySignal)
class VehicleAvailabilitySignalAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "hub", "signal", "is_available", "updated_at")
    list_filter = ("signal", "is_available", "hub")
    search_fields = ("vehicle__name", "hub__name")


from .models import ParkingLocation

@admin.register(ParkingLocation)
class ParkingLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'latitude', 'longitude')
    search_fields = ('name', 'city')

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_type', 'subject', 'user_name', 'status', 'created_at')
    list_filter = ('status', 'ticket_type')
    search_fields = ('subject', 'message', 'user_name', 'user_contact')

@admin.register(HostVehicle)
class HostVehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'registration_number', 'vehicle_type', 'status', 'created_at')
    list_filter = ('status', 'vehicle_type')
    search_fields = ('brand', 'model_name', 'registration_number', 'owner_name')

from django.core.mail import send_mail
from django.contrib import messages

@admin.register(CancellationRequest)
class CancellationRequestAdmin(admin.ModelAdmin):
    list_display = ('booking', 'reason', 'status', 'created_at', 'admin_actions')
    list_filter = ('status', 'created_at')
    search_fields = ('booking__full_name', 'booking__email', 'reason')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:req_id>/accept/', self.admin_site.admin_view(self.accept_cancellation), name='cancellation-accept'),
            path('<int:req_id>/reject/', self.admin_site.admin_view(self.reject_cancellation), name='cancellation-reject'),
        ]
        return custom_urls + urls

    def accept_cancellation(self, request, req_id):
        from django.core.mail import EmailMultiAlternatives
        from django.utils.html import strip_tags
        from email.mime.image import MIMEImage
        import os
        from django.conf import settings
        
        try:
            req = CancellationRequest.objects.get(id=req_id)
            req.status = 'Accepted'
            req.save()
            
            booking = req.booking
            booking.status = 'Cancelled'
            booking.save()
            
            subject = f"🚗 DriveGO: Refund Initiated for {booking.vehicle_name}"
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #0f1422; margin: 0; padding: 20px; color: #f8fafc; -webkit-font-smoothing: antialiased; }}
                    .container {{ width: 100%; max-width: 500px; margin: 40px auto; background: rgba(30, 41, 59, 0.3); border-radius: 20px; overflow: hidden; border: 1px solid rgba(255, 255, 255, 0.05); }}
                    .header {{ padding: 35px 30px 20px; text-align: center; }}
                    .content {{ padding: 0 35px 35px; text-align: center; }}
                    .greeting {{ font-size: 22px; font-weight: 700; margin-bottom: 12px; color: #ffffff; letter-spacing: -0.2px; line-height: 1.4; }}
                    .subtitle {{ line-height: 1.6; color: #94a3b8; font-size: 13px; margin-bottom: 30px; padding: 0 10px; }}
                    .details-box {{ background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 30px; margin: 0 auto; max-width: 400px; text-align: center; }}
                    .refund-title {{ color: #64748b; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; }}
                    .refund-amount {{ font-weight: 700; color: #ffffff; font-size: 42px; line-height: 1; margin: 10px 0 30px; letter-spacing: -0.5px; }}
                    .divider {{ height: 1px; background: rgba(255,255,255,0.05); margin: 0 0 20px 0; }}
                    .label {{ color: #64748b; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
                    .value {{ font-weight: 500; color: #f8fafc; font-size: 13px; text-align: right; }}
                    .status-badge {{ color: #10b981; font-weight: 500; }}
                </style>
            </head>
            <body>
                <div style="background: #0f1422; padding: 40px 20px; min-height: 100vh;">
                    <div class="container">
                        <div class="header">
                            <h1 style="font-size: 18px; font-weight: 700; color: #60a5fa; margin: 0; letter-spacing: -0.5px;">
                                Drive<span style="color: #3b82f6; font-size: 14px; vertical-align: middle; margin-left: 1px;">●</span>
                            </h1>
                        </div>
                        <div class="content">
                            <div class="greeting">Refund Initiated,<br>{booking.full_name}!</div>
                            <p class="subtitle">
                                Your cancellation request has been <span style="color: #10b981; font-weight: 600;">accepted</span> by<br>the Admin. We have successfully initiated your<br>refund to your original payment method.
                            </p>
                            
                            <div class="details-box">
                                <div class="refund-title">Total Refund Amount</div>
                                <div class="refund-amount">₹{booking.total_amount}</div>
                                <div class="divider"></div>
                                <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                    <tr>
                                        <td class="label" align="left" style="padding-bottom: 12px;">Vehicle</td>
                                        <td class="value" align="right" style="padding-bottom: 12px;">{booking.vehicle_name}</td>
                                    </tr>
                                    <tr>
                                        <td class="label" align="left">Status</td>
                                        <td class="value status-badge" align="right" style="color: #10b981;">Processed</td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(
                subject, 
                text_content,
                getattr(settings, 'EMAIL_HOST_USER', 'noreply@drivego.com'),
                [booking.email]
            )
            msg.attach_alternative(html_content, "text/html")
            
            logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo_transparent.png')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_img = MIMEImage(f.read())
                    logo_img.add_header('Content-ID', '<logo_transparent>')
                    logo_img.add_header('Content-Disposition', 'inline', filename='logo_transparent.png')
                    msg.attach(logo_img)
                    
            msg.send(fail_silently=False)
            
            messages.success(request, 'Cancellation Accepted, Booking Cancelled, and Refund Email sent!')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect(request.META.get('HTTP_REFERER', 'admin:MyApp_cancellationrequest_changelist'))

    def reject_cancellation(self, request, req_id):
        try:
            req = CancellationRequest.objects.get(id=req_id)
            req.status = 'Rejected'
            req.save()
            messages.warning(request, 'Cancellation Rejected.')
        except Exception as e:
            messages.error(request, f'Error: {e}')
        return redirect(request.META.get('HTTP_REFERER', 'admin:MyApp_cancellationrequest_changelist'))

    def admin_actions(self, obj):
        return format_html(
            '<a class="button" style="background:linear-gradient(135deg, #10b981, #059669) !important; color:#ffffff !important; margin-right:5px; padding:6px 12px; border:none !important;" href="{}">Accept</a>'
            '<a class="button" style="background:linear-gradient(135deg, #ef4444, #dc2626) !important; color:#ffffff !important; padding:6px 12px; border:none !important;" href="{}">Reject</a>',
            reverse('admin:cancellation-accept', args=[obj.id]),
            reverse('admin:cancellation-reject', args=[obj.id]),
        )
    admin_actions.short_description = 'Actions'
