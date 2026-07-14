# from email.mime import message
# from pyexpat import model
from django.http import Http404, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from psycopg.pq import error_message
from django.core.files.storage import FileSystemStorage

import stripe
from django.conf import settings as django_settings  # Rename to avoid function conflicts

from django.shortcuts import render
from .models import Booking






from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage
import json





import stripe
from django.conf import settings

from .models import Booking





# In MyApp/views.py
from django.shortcuts import render, get_object_or_404
from .models import Vehicle # Replace 'Vehicle' with your actual Model name


from django.http import HttpRequest


import re


from .models import CarBooking # Import your model








from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


from .models.cars import Car
from .models.orders import Order
from .models.category import Category

from .models.customer import Customer
from .models.contact import Contact



from django.shortcuts import render
from .models.vehicle import Vehicle
from .models import RentalHub, VehicleAvailabilitySignal




def index(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}

    # Get all categories
    categories = Category.get_all_categories()

    # Get selected category from URL (?category=)
    categoryID = request.GET.get('category')

    # Filter vehicles
    if categoryID:
        vehicles = Vehicle.get_all_vehicles_by_categoryid(categoryID)
    else:
        vehicles = Vehicle.get_all_vehicles()

    data = {
        'vehicles': vehicles,
        'categories': categories
    }

    print("You are:", request.session.get('email'))
    return render(request, 'index.html', data)






#2nd
def signup(request):

    if request.method == "POST":

        # get fields (use same names as your HTML inputs)

        name = request.POST.get('name', '').strip()

        username = request.POST.get('username', '').strip()

        number = request.POST.get('number', '').strip()

        email = request.POST.get('email', '').strip()

        password = request.POST.get('password', '')

        password2 = request.POST.get('password2', '')



        # Basic validation

        if not username:

            messages.error(request, "Username is required.")

            return render(request, 'signup.html')



        if not email:

            messages.error(request, "Email is required.")

            return render(request, 'signup.html')



        if password != password2:

            messages.error(request, "Passwords do not match.")

            return render(request, 'signup.html')



        # Check existing username/email

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already taken.")

            return render(request, 'signup.html')



        if User.objects.filter(email=email).exists():

            messages.error(request, "Email already taken.")

            return render(request, 'signup.html')



        # Create the auth User (this hashes the password for you)

        user = User.objects.create_user(username=username, email=email, password=password)

        user.first_name = name  # optional, store full name in first_name or split it

        user.save()

       

       

       



        customer = Customer(

            name=name,

            username=username,

            number=number,

            email=email,

            password=password,          # save password directly

            re_enter_password=password2 # also save confirm password

           

         )

        customer.register()

        auth_login(request, user)
        messages.success(request, "Account created successfully. You are now logged in.")
        return redirect('index')



    # GET request => show signup form

    return render(request, 'signup.html') 


#...................
def payment_view(request):
    # Retrieve the final payment amount (You would typically get this from a session or database)
    payment_amount = 4520 

    if request.method == 'POST':
        # --- 1. Document Upload Handling ---
        
        # Files are accessed via request.FILES
        aadhaar_file = request.FILES.get('aadhaar-file')
        dl_file = request.FILES.get('dl-file')
        
        if not aadhaar_file or not dl_file:
            messages.error(request, "Both Aadhaar Card and Driving License files are required.")
            return render(request, 'payment_verification.html', {'amount': payment_amount})
            
        # Example: Saving files to the media folder
        # NOTE: You should use a proper FileSystemStorage or cloud storage in production
        fs = FileSystemStorage()
        try:
            aadhaar_filename = fs.save(f'documents/{request.user.username}_aadhaar_{aadhaar_file.name}', aadhaar_file)
            dl_filename = fs.save(f'documents/{request.user.username}_dl_{dl_file.name}', dl_file)
            # You would save these filenames/paths to your database model here
            # e.g., Booking.objects.get(user=request.user).aadhaar_path = aadhaar_filename
        except Exception as e:
            messages.error(request, f"File upload failed: {e}")
            return render(request, 'payment_verification.html', {'amount': payment_amount})


        # --- 2. Payment Data Handling ---
        
        # Get selected payment method
        payment_method = request.POST.get('payment_method')
        
        # Example: Card details (only for mock or sending to a secure gateway)
        if payment_method == 'cards':
            card_number = request.POST.get('card-number')
            card_name = request.POST.get('card-name')
            expiry = request.POST.get('expiry')
            cvv = request.POST.get('cvv')
            # In a real application, these would be sent directly to a payment gateway (e.g., Stripe, Razorpay) 
            # over a secure API connection, not saved in your database.
            
        # Example: UPI details
        elif payment_method == 'upi':
            upi_id = request.POST.get('upi-id')
            # Logic to initiate UPI transaction via a payment gateway
        
        # --- 3. Final Processing and Redirect ---
        
        # MOCK SUCCESS: If all validations and (mock) payment initiation passed:
        messages.success(request, "Payment initiated and documents uploaded successfully. Please complete the transaction.")
        
        # Redirect to a success/thank you page (or the payment gateway's URL)
        return redirect('thankyou') 

    # Handle GET request (initial page load)
    return render(request, 'payment_verification.html', {'amount': payment_amount})
        
        
        
     
     
     #bill
def order(request):
    if request.method == "POST":
        billname = request.POST.get('billname','')
        billemail = request.POST.get('billemail','')
        billphone = request.POST.get('billphone','')
        billaddress = request.POST.get('billaddress','')
        billcity = request.POST.get('billcity','')
        cars11 = request.POST['cars11']
        dayss = request.POST.get('dayss','')
        date = request.POST.get('date','')
        fl = request.POST.get('fl','')
        tl = request.POST.get('tl','')
        # print(request.POST['cars11'])
        
        order = Order(name = billname,email = billemail,phone = billphone,address = billaddress,city=billcity,cars = cars11,days_for_rent = dayss,date = date,loc_from = fl,loc_to = tl)
        order.save()
        return redirect('home')
    else:
        print("error")
    
        return render(request,'bill.html')
    
    
    #contact
def contact(request):
    if request.method == "POST":
        contactname = request.POST.get('contactname','')
        contactemail = request.POST.get('contactemail','')
        contactnumber = request.POST.get('contactnumber','')
        contactmsg = request.POST.get('contactmsg','')

        contact = Contact(name = contactname, email = contactemail, phone_number = contactnumber,message = contactmsg)
        contact.save()
    return render(request,'contact.html ')

#signin


def signin(request):
    if request.method == "POST":
        loginusername = request.POST.get('loginusername', '').strip()
        loginpassword = request.POST.get('loginpassword', '')

        if not loginusername or not loginpassword:
            messages.error(request, "Please enter both username and password.")
            return render(request, 'login.html')

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            auth_login(request, user)        # use auth_login to avoid name collision
            messages.success(request, "Successfully logged in!")
            return redirect('vehicles')     # ensure 'vehicles' URL name exists
        else:
            messages.error(request, "Invalid credentials.")
            return render(request, 'login.html')

    # GET request
    return render(request, 'login.html')
    
    
    #vechicles


def vehicles(request):
    # ensure cart session exists
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}

    categories = Category.get_all_categories()

    # category parameter from the URL e.g. /vehicles/?category=3
    category_param = request.GET.get('category')  # could be '3' or maybe category name

    # Best: template should send category id. Try to coerce to int if possible.
    category_id = None
    if category_param:
        try:
            category_id = int(category_param)
        except ValueError:
            # if the template sent a name instead of id, try to find the category by name
            try:
                cat = Category.objects.filter(name__iexact=category_param).first()
                if cat:
                    category_id = cat.id
            except Exception:
                category_id = None

    # get vehicles using model helper
    vehicles = Vehicle.get_all_vehicles_by_categoryid(category_id)

    data = {
        'vehicles': vehicles,        # lowercase key --> use this name in template
        'categories': categories,
        'selected_category_id': category_id,  # optional: to mark selected option in template
    }

    print('you are : ', request.session.get('email'))
    print('category_param:', category_param, 'resolved category_id:', category_id)

    return render(request, 'vehicles.html', data)



def luxury(request):
    # Filter luxury vehicles or show a page
    vehicles = Vehicle.objects.filter(category__name__iexact='luxury')
    return render(request, 'luxury.html', {'vehicles': vehicles})


def bikes(request):
    vehicles = Vehicle.objects.filter(category__name__iexact='bike')
    return render(request, 'bikes.html', {'vehicles': vehicles})

def scooters(request):
    vehicles = Vehicle.objects.filter(category__name__iexact='scoty')
    return render(request, 'scooters.html', {'vehicles': vehicles})


def location_tracking(request):
    hubs = RentalHub.objects.filter(is_active=True).order_by("name")
    selected_hub_id = request.GET.get("hub")
    selected_hub = None
    signals = VehicleAvailabilitySignal.objects.none()

    if selected_hub_id:
        try:
            selected_hub = hubs.get(id=selected_hub_id)
            signals = (
                VehicleAvailabilitySignal.objects.filter(hub=selected_hub)
                .select_related("vehicle", "hub")
                .order_by("vehicle__name")
            )
        except RentalHub.DoesNotExist:
            selected_hub = None

    context = {
        "hubs": hubs,
        "selected_hub": selected_hub,
        "signals": signals,
    }
    return render(request, "location_tracking.html", context)


def location_signals_api(request):
    hub_id = request.GET.get("hub")
    if not hub_id:
        return JsonResponse({"error": "hub parameter is required"}, status=400)

    try:
        hub = RentalHub.objects.get(id=hub_id, is_active=True)
    except RentalHub.DoesNotExist:
        return JsonResponse({"error": "Invalid hub selected"}, status=404)

    signals = (
        VehicleAvailabilitySignal.objects.filter(hub=hub)
        .select_related("vehicle")
        .order_by("vehicle__name")
    )

    data = [
        {
            "vehicle_name": signal.vehicle.name,
            "signal": signal.signal,
            "is_available": signal.is_available,
            "lat": float(hub.latitude),
            "lng": float(hub.longitude),
        }
        for signal in signals
    ]
    return JsonResponse({"hub": hub.name, "signals": data})


    
    
    
    
  

from django.contrib.auth import update_session_auth_hash

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    if request.method == 'POST':
        old_password = request.POST.get('current-password')
        new_password = request.POST.get('new-password')
        confirm_password = request.POST.get('confirm-password')

        if not request.user.check_password(old_password):
            messages.error(request, "Current password is not correct.")
        elif new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Password updated successfully.")
            return redirect('profile')

    return render(request, 'changepassword.html')  

def logout_user(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('index')

def payment_view(request):
    """View to render the payment.html page"""
    return render(request, 'payment.html')
    
    
  


def offers(request):
    return render(request, 'offers.html')     
     
     
     
     
     
def Login(request):
    return render(request, 'login.html')     
     
def lock(request):
    return render(request, 'lock.html')

def key(request):
    return render(request, 'key.html')
     
def host(request):
    return render(request, 'host.html')


     
def Services(request):
    return render(request, 'Services.html')
     
     
     


def bbase(request):
	return render(request,'bbase.html')


def car_listing(request):
    return render(request,'car-listing.html')



def activity(request):
    from MyApp.models import Vehicle
    if request.user.is_authenticated:
        recent_bookings = list(Booking.objects.filter(user=request.user).order_by('-created_at')[:10])
    else:
        recent_bookings = []
    
    # Process bookings to attach vehicle image URL dynamically
    processed_bookings = []
    for b in recent_bookings:
        v = Vehicle.objects.filter(name=b.vehicle_name).first()
        # Create a dictionary to hold all info easily inside template
        booking_data = {
            'obj': b,
            'image_url': v.image.url if (v and hasattr(v, 'image') and v.image) else '',
        }
        processed_bookings.append(booking_data)
        
    return render(request, 'activity.html', {'bookings': processed_bookings})

def account(request):
    return render(request,'account.html')

def vehicle_details(request):
    return render(request,'vehicle-details.html')

def booking_summary(request):
    context = {'default_city': request.GET.get('city', 'India')}
    return render(request,'booking-summary.html', context)

def booking_success(request):
    return render(request,'booking-success.html')

def bill(request):
    return render(request,'bill.html')


def account(request):
    return render(request,'account.html')

def membership(request):
    return render(request, 'membership.html')



def settings(request):
    return render(request, 'settings.html')

from .models.user_profile import UserProfile
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        request.user.first_name = request.POST.get('fullName', request.user.first_name)
        request.user.save()
        
        profile.license_number = request.POST.get('license', profile.license_number)
        profile.phone = request.POST.get('phone', profile.phone)
        profile.address = request.POST.get('address', profile.address)
        profile.emergency_contact_name = request.POST.get('emergency_contact_name', profile.emergency_contact_name)
        profile.emergency_contact_phone = request.POST.get('emergency_contact_phone', profile.emergency_contact_phone)
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES and request.FILES['profile_picture']:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
        
    return render(request, 'profile.html', {'profile': profile})

def help(request):
    return render(request, 'help.html')

def support(request):
    return render(request, 'support.html')

def report_issue(request):
    return render(request, 'report_issue.html')

from .models import SupportTicket, HostVehicle
from django.contrib import messages

def support_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        email = request.POST.get('email')
        
        SupportTicket.objects.create(
            ticket_type='Email',
            subject=subject,
            message=message,
            user_contact=email
        )
        return redirect('activity')
    return render(request, 'support_email.html')

def support_call(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        phone = request.POST.get('phone')
        
        SupportTicket.objects.create(
            ticket_type='Call',
            subject=subject,
            message=message,
            user_contact=phone
        )
        return redirect('activity')
    return render(request, 'support_call.html')

def host_vehicle(request):
    if request.method == 'POST':
        vehicle_type = request.POST.get('vehicle_type')
        brand = request.POST.get('brand')
        model_name = request.POST.get('model_name')
        registration_number = request.POST.get('registration_number')
        rental_price = request.POST.get('rental_price')
        vehicle_photo = request.FILES.get('vehicle_photo')
        
        HostVehicle.objects.create(
            vehicle_type=vehicle_type,
            brand=brand,
            model_name=model_name,
            registration_number=registration_number,
            rental_price=rental_price,
            vehicle_photo=vehicle_photo
        )
        return redirect('index')
    return render(request, 'host.html')

def thankyou(request):
    return render(request, 'thankyou.html')



def confirm(request):
    return render(request,'confirm.html')








from django.shortcuts import render, get_object_or_404
from .models import Vehicle  # Ensure your model name is correct

def booking_summary(request, vehicle_id):
    # Fetch the specific car based on the ID passed from the previous page
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    context = {
        'v': vehicle,
        'tax_fee': 250,
        'discount': 200,
        'default_city': request.GET.get('city', 'India')
    }
    return render(request, 'booking_summary.html', context)






def success_view(request):
    return render(request, 'success.html')


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import threading

def send_email_booking_confirmation(email_address, name, vname, pickup, ret, total):
    """
    Automated background task to send a beautifully styled HTML email receipt.
    """
    if not email_address:
        print("No email address provided for booking. Skipping email dispatch.")
        return

    try:
        from django.conf import settings
        
        subject = f"🚗 DriveGO Booking Confirmed: {vname}"
        
        # DriveGO Styled HTML Email (Matching OTP Theme)
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 20px; color: #1e293b; -webkit-font-smoothing: antialiased; }}
                .container {{ width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }}
                .header {{ padding: 35px 30px; text-align: center; background: linear-gradient(to right, #f8fafc, #f1f5f9); border-bottom: 1px solid #e2e8f0; }}
                .content {{ padding: 40px 30px; text-align: center; }}
                .greeting {{ font-size: 24px; font-weight: 700; margin-bottom: 15px; color: #0f172a; }}
                .details-box {{ background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border: 2px dashed #7dd3fc; border-radius: 16px; padding: 30px; margin: 30px auto; max-width: 400px; box-shadow: 0 4px 15px rgba(14, 165, 233, 0.1); text-align: left; }}
                .detail-row {{ display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px dashed rgba(14, 165, 233, 0.3); }}
                .detail-row:last-child {{ border-bottom: none; }}
                .label {{ color: #0369a1; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }}
                .value {{ font-weight: 800; color: #0f172a; font-size: 15px; text-align: right; }}
                .value.highlight {{ color: #0ea5e9; font-size: 20px; }}
                .footer {{ padding: 35px 30px; background-color: #0f172a; color: #94a3b8; text-align: center; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div style="background-color: #f1f5f9; padding: 40px 20px;">
                <div class="container">
                    <div class="header">
                        <img src="cid:logo_transparent" alt="DriveGO" style="max-height: 60px; display: block; margin: 0 auto; border: 0;" onerror="this.style.display='none'; document.getElementById('fallback-logo').style.display='block';">
                        <h1 id="fallback-logo" style="display: none; font-size: 36px; font-weight: 900; color: #1e293b; margin: 0; letter-spacing: -1px;">
                            <span style="color: #0ea5e9;">Drive</span><span style="color: #1e293b;">GO</span>
                        </h1>
                    </div>
                    <div class="content">
                        <div class="greeting">Booking Confirmed, {name}! 🚗</div>
                        <p style="margin-bottom: 25px; line-height: 1.6; color: #475569;">
                            Your ride is ready. Thank you for choosing <strong>DriveGO</strong>, your premier smart self-drive vehicle rental platform. Below are the details of your confirmed booking:
                        </p>
                        
                        <div class="details-box">
                            <div class="detail-row">
                                <span class="label">Vehicle</span>
                                <span class="value">{vname}</span>
                            </div>
                            <div class="detail-row">
                                <span class="label">Total Paid</span>
                                <span class="value highlight">₹{total}</span>
                            </div>
                            <div class="detail-row">
                                <span class="label">Pickup Date</span>
                                <span class="value">{pickup}</span>
                            </div>
                            <div class="detail-row">
                                <span class="label">Return Date</span>
                                <span class="value">{ret}</span>
                            </div>
                        </div>
                        
                        <p style="text-align: center; font-weight: 600; color: #1e293b; margin-top: 30px;">
                            Safe travels and enjoy your ride!
                        </p>
                    </div>
                    <div class="footer">
                        <h4 style="color: #f8fafc; margin-top: 0; margin-bottom: 10px; font-size: 18px; font-weight: 600; letter-spacing: 0.5px;">Experience Freedom on Wheels</h4>
                        <p style="margin: 0 0 15px 0; font-size: 14px; line-height: 1.5; color: #cbd5e1;">
                            DriveGO is revolutionizing the smart self-drive vehicle rental system. Book seamlessly, unlock instantly, and hit the road.
                        </p>
                        <div style="height: 1px; background-color: #334155; margin: 20px 0;"></div>
                        <p style="margin: 0; color: #475569; font-size: 12px;">&copy; 2026 DriveGO. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        from django.core.mail import EmailMultiAlternatives
        from django.utils.html import strip_tags
        from email.mime.image import MIMEImage
        import os
        
        text_content = strip_tags(html_content)
        
        msg = EmailMultiAlternatives(
            subject, 
            text_content,
            getattr(settings, 'EMAIL_HOST_USER', 'noreply@drivego.com'),
            [email_address]
        )
        msg.attach_alternative(html_content, "text/html")
        
        # Embed transparent logo inline
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo_transparent.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_img = MIMEImage(f.read())
                logo_img.add_header('Content-ID', '<logo_transparent>')
                logo_img.add_header('Content-Disposition', 'inline', filename='logo_transparent.png')
                msg.attach(logo_img)
                
        msg.send(fail_silently=False)
        print(f"Receipt email successfully sent to {email_address} with embedded logo.")
        
    except Exception as e:
        print(f"Failed to send automated email: {str(e)}")

def create_stripe_session(request):
    if request.method == 'POST':
        try:
            # 1. Capture All Data from the Request
            name = request.POST.get('name', 'Guest')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            vname = request.POST.get('vname', 'Vehicle')
            location = request.POST.get('location', '')
            color = request.POST.get('color', '')
            pickup = request.POST.get('pickup')
            return_date = request.POST.get('return')
            total = request.POST.get('total', '0').replace(',', '')

            pay_method = request.POST.get('payment_method')
            c_num = request.POST.get('card_number')
            u_id = request.POST.get('upi_id')

            # 2. SAVE TO ADMIN FIRST (Crucial)
            # This ensures all booking summary and payment details are stored immediately
            booking = Booking.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=name,
                email=email,
                phone=phone,
                vehicle_name=vname,
                location=location,
                color=color,
                pickup_date=pickup if pickup else None,
                return_date=return_date if return_date else None,
                total_amount=float(total),
                aadhaar_card=request.FILES.get('aadhaar'),
                driving_license=request.FILES.get('dl'),
                payment_method=pay_method,
                card_number=c_num,
                upi_id=u_id,
                status='Pending'
            )

            # --- AUTOMATED EMAIL DISPATCH ---
            # Spawn a background thread to send the HTML email immediately after saving to DB
            threading.Thread(target=send_email_booking_confirmation, args=(
                email, name, vname, pickup if pickup else 'Today', return_date if return_date else 'Later', total
            )).start()

            # 3. Attempt Stripe Checkout
            # If this fails (e.g., due to the 'sk_test_**P...' error), the 'except' block handles it.
            stripe.api_key = settings.STRIPE_SECRET_KEY
            amount_in_paise = int(float(total) * 100)
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {'name': f'DriveGO: {vname}'},
                        'unit_amount': amount_in_paise,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/payment/'),
            )

            # Update booking with Stripe ID if successful
            booking.stripe_checkout_id = checkout_session.id
            booking.save()

            return JsonResponse({'id': checkout_session.id})

        except Exception as e:
            # SILENT ERROR FIX: 
            # We return a 200 status with 'id': None so your JavaScript 
            # knows to ignore the error and redirect directly to /success/
            print(f"Stripe Error caught: {str(e)}") # Log error for your info
            return JsonResponse({'message': 'Data Saved to Admin', 'id': None}, status=200)






# This is the view that will handle the form submission
def process_booking(request):
    if request.method == 'POST':
        # 1. Get data from the submitted form (using the 'name' attributes from HTML)
        full_name = request.POST.get('billname')
        email = request.POST.get('billemail')
        phone_number = request.POST.get('billphone')
        car_chosen = request.POST.get('car_chosen')
        car_color = request.POST.get('car_color')
        
        # Convert strings to correct types
        num_days = int(request.POST.get('num_days', 0))
        pickup_date = request.POST.get('pickup_date')
        total_rent = float(request.POST.get('total_rent', 0.0))
        
        from_location = request.POST.get('from_location')
        to_location = request.POST.get('to_location')
        
        # 2. Create and save a new Booking object in the database
        CarBooking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone_number=phone_number,
            car_chosen=car_chosen,
            car_color=car_color,
            num_days=num_days,
            pickup_date=pickup_date,
            from_location=from_location,
            to_location=to_location,
            total_rent=total_rent
        )
        
        # 3. Redirect the user to a thank you page after successful submission
        return redirect('thankyou_page') # Use the actual URL name for your thank you page
        
    # If it's a GET request, just render the booking page
    return render(request, 'bill.html')

# Simple example view for the thank you page
def thankyou_page(request):
    return HttpResponse("<h1>Thank You for your booking!</h1><p>Your details have been saved to the admin page.</p>")
















@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        msg = user_message.lower()
        reply = ""

        # --- MODULE 1: PLATFORM UTILITY & AI QUESTIONS ---
        if any(x in msg for x in ["use of this rental", "why use drivego", "benefit"]):
            reply = "<b>DriveGO</b> provides 24/7 access to premium vehicles with <b>doorstep delivery</b>, all-India permits, and zero maintenance costs."
        elif any(x in msg for x in ["use of ai chatbot", "ai purpose", "what can you do"]):
            reply = "I am your <b>Digital Concierge</b>. I manage live pricing, document verification, voice-based extensions, and IoT car controls."
        elif any(x in msg for x in ["how to book", "steps to book", "booking process"]):
            reply = "<b>3 Steps:</b> 1. Select vehicle, 2. Upload Aadhaar/License for verification, 3. Pay via UPI/Card."

        # --- MODULE 2: ADMIN & FLEET MANAGEMENT (! Commands) ---
        elif msg.startswith("!add_vehicle"):
            reply = "<b>Admin Action:</b> New vehicle added to fleet. Details captured for effective management."
        elif msg.startswith("!update_vehicle_availability"):
            reply = "<b>System Update:</b> Vehicle status updated to real-time availability."
        elif msg.startswith("!list_available_vehicles"):
            reply = "<b>Fleet Status:</b> Fetching all vehicles ready for immediate rental."
        elif msg.startswith("!record_vehicle_maintenance") or msg.startswith("!schedule_maintenance"):
            reply = "<b>Maintenance Log:</b> Service recorded/scheduled to ensure optimal vehicle condition."
        elif msg.startswith("!add_rental_office"):
            reply = "<b>Logistics:</b> New rental office location added to the DriveGO network."

        # --- MODULE 3: USER ACCOUNT & REGISTRATION ---
        elif any(x in msg for x in ["signup", "!register_customer", "create account"]):
            reply = "Registration initiated. Proper registration is essential for tracking activity and personalized service."
        elif any(x in msg for x in ["update_profile", "!update_customer_contact", "change email"]):
            reply = "Profile update triggered. Keeping contact info current ensures effective service delivery."
        elif "upload_documents" in msg or "verify" in msg:
            reply = "Please upload your <b>Aadhaar</b> and <b>Driving License</b>. Min age 21."

        # --- MODULE 4: SEARCH, DISCOVERY & RECOMMENDATIONS ---
        elif any(x in msg for x in ["search", "find_car", "near me", "available"]):
            reply = "Scanning real-time options. You can choose based on budget, seating, or transmission."
        elif any(x in msg for x in ["best car", "recommendation", "suggest"]):
            reply = "<b>Tailored Choice:</b> Based on your trip, I recommend the <b>Lambgini</b> for thrills or <b>SUV</b> for family."
        elif "luxury" in msg or "supercar" in msg:
            reply = "Our Elite collection (Lambgini/Rolls) is capped at 120km/hr for safety."

        # --- MODULE 5: BOOKING & TRIP MANAGEMENT ---
        elif any(x in msg for x in ["book_car", "rent a car", "!assign_vehicle", "need a vehicle"]):
            reply = "Booking initiated. Assigning vehicle to your ID for the requested rental period."
        elif any(x in msg for x in ["extend", "modify", "change_drop"]):
            reply = "Modification active. You can adjust dates or drop locations via the chatbot."
        elif any(x in msg for x in ["cancel", "refund", "money back"]):
            reply = "Cancellation policy: Full refund >24hrs, 50% within 24hrs, no refund after start."
        elif "start_trip" in msg or "end_trip" in msg:
            reply = "Trip status updated. Ensure fuel is 'Full-to-Full' to avoid surcharges."

        # --- MODULE 6: PAYMENT & INVOICING ---
        elif any(x in msg for x in ["payment", "!add_payment_method", "upi", "card"]):
            reply = "Payment method added. We use secure transactions for all DriveGO bookings."
        elif any(x in msg for x in ["invoice", "!generate_invoice", "download receipt"]):
            reply = "Invoice generated. Transparency is our priority for all rental periods."

        # --- MODULE 7: SMART IoT CONTROLS ---
        elif any(x in msg for x in ["unlock_car", "lock_car", "start_engine", "honk"]):
            reply = "<b>IoT Command:</b> Connection established with vehicle. Action performed successfully."
        elif "fuel_status" in msg or "battery_status" in msg:
            reply = "Fetching real-time telematics. Your fuel level is updated on your dashboard."

        # --- MODULE 8: SERVICES & OFFERS ---
        elif "long-term" in msg or "subscription" in msg:
            reply = "<b>Services:</b> Weekly and monthly plans available with insurance included."
        elif "one-way" in msg:
            reply = "<b>Services:</b> Pick up in Delhi, drop in Noida. Drop-off fee applies."
        elif "corporate" in msg:
            reply = "<b>Corporate:</b> Special packages for business clients with GST billing."
        elif "offers" in msg or "discount" in msg:
            reply = "Check your notifications for exclusive promotional deals and seasonal offers."
            
        if any(x in msg for x in ["use of this rental", "why use drivego", "benefit"]):
            reply = """<b>Why DriveGO?</b><br>
            We provide 24/7 access to premium vehicles without the cost of ownership. 
            Enjoy <b>doorstep delivery</b>, <b>all-India permits</b>, and <b>insurance-backed</b> rides."""

        elif any(x in msg for x in ["use of ai chatbot", "what can you do", "ai purpose"]):
            reply = """<b>I am your Digital Concierge!</b><br>
            I help you:<br>
            • Check <b>Live Prices</b> and <b>Availability</b>.<br>
            • Explain <b>Damage & Fuel Policies</b>.<br>
            • Guide you through <b>Document Uploads</b>.<br>
            • Handle <b>Extensions</b> via voice/text commands."""

        elif any(x in msg for x in ["how to book", "steps to book", "booking process"]):
            reply = """<b>3 Simple Steps to your Ride:</b><br>
            1. <b>Select:</b> Pick your vehicle from the Home/Luxury tab.<br>
            2. <b>Verify:</b> Upload your Aadhaar & License in the Payment section.<br>
            3. <b>Pay:</b> Confirm your slot with UPI or Card. Your ride is ready!"""

        elif any(x in msg for x in ["which car is best", "recommendation", "suggest a car"]):
            reply = """<b>Our Recommendations:</b><br>
            • <b>For Thrill:</b> The <b>Lambgini</b> (₹250/hr).<br>
            • <b>For Class:</b> The <b>Rolls-Royce Ghost</b> (₹250/hr).<br>
            • <b>For City:</b> Our <b>Electric Scooters</b> (₹40/hr).<br>
            What is your vibe today, Venn?"""

        # 2. NEW: SERVICES (Long-term, One-way, Corporate)
        elif any(x in msg for x in ["long term", "subscription", "monthly", "weekly"]):
            reply = """<b>DriveGO Subscriptions:</b><br>
            Save up to 30% with our long-term plans. We offer <b>Weekly</b> and <b>Monthly</b> subscriptions with free maintenance and insurance included."""

        elif any(x in msg for x in ["one way", "different city", "intercity drop"]):
            reply = """<b>One-Way Trips:</b><br>
            Pick up in Delhi and drop off in Noida or Gurgaon! Select the 'One-Way' toggle during booking (Additional 'Drop-off fee' may apply)."""

        elif any(x in msg for x in ["corporate", "business", "company plan", "office"]):
            reply = """<b>Corporate Packages:</b><br>
            Special GST-ready billing and discounted rates for business clients. Contact <b>corp@drivego.com</b> for a dedicated account manager."""

        elif any(x in msg for x in ["add-on", "gps", "child seat", "extra"]):
            reply = """<b>Vehicle Add-ons:</b><br>
            You can add <b>GPS Navigation</b>, <b>Child Seats</b>, or <b>Action Cameras</b> at the 'Booking Summary' page for a small daily fee."""

        # 3. NEW: PROFILE & ACTIVITY DETAILS
        elif any(x in msg for x in ["my profile", "account details", "edit info"]):
            reply = "You can manage your saved documents, linked cards, and personal info in the <b>Profile Tab</b> at the bottom right of the app."

        elif any(x in msg for x in ["my booking", "activity", "current ride", "status"]):
            reply = "Check your <b>Activity Tab</b> to see active, upcoming, and past bookings. You can also download invoices there."

        # 4. EXISTING COMMANDS (Maintained & Updated)
        elif any(x in msg for x in ["price", "cost", "how much", "rate", "deposit", "fare"]):
            reply = """<b>Pricing Structure:</b><br>
            • <b>Luxury:</b> ₹250/hr (₹2,000 Deposit)<br>
            • <b>Premium:</b> ₹220/hr (₹1,500 Deposit)<br>
            • <b>Scooters:</b> ₹40/hr (₹500 Deposit)"""

        elif any(x in msg for x in ["speed", "limit", "how fast"]):
            reply = """<b>Speed Limits:</b><br>
            • <b>Luxury Cars:</b> Capped at 120km/hr.<br>
            • <b>Bikes:</b> Capped at 80km/hr.<br>
            Safety first! Speeding triggers a ₹1,000 fine via GPS tracking."""

        elif any(x in msg for x in ["doc", "id", "license", "aadhaar", "passport"]):
            reply = "<b>Requirements:</b> Minimum age 21, Original Permanent DL, and Aadhaar/Passport are mandatory."

        elif any(x in msg for x in ["fuel", "petrol", "diesel", "refill"]):
            reply = "<b>Fuel Policy:</b> Full-to-Full. Return with a full tank to avoid service charges."

        elif any(x in msg for x in ["accident", "damage", "scratch", "dent"]):
            reply = "<b>Damage:</b> Minor scratches capped at ₹5,000. For major issues, call <b>1800-DRIVE-GO</b> immediately."

        elif any(x in msg for x in ["cancel", "refund", "money back"]):
            reply = "<b>Refunds:</b> Full refund if cancelled >24hrs before trip. 50% refund within 24hrs."

        elif any(x in msg for x in ["hi", "hello", "hey", "who are you"]):
            reply = f"Hello <b>Venn</b>! 🚗 I'm your DriveGO AI. Ask me about <b>Booking Steps</b>, <b>Corporate Plans</b>, or <b>Luxury Car Specs</b>!"    

        # --- MODULE 9: SUPPORT & SAFETY ---
        elif any(x in msg for x in ["help", "support", "emergency", "breakdown"]):
            reply = "24/7 Support: Call <b>1800-DRIVE-GO</b> for roadside assistance or accidents."
        elif "speed" in msg or "limit" in msg:
            reply = "Safety: Speeding triggers a ₹1,000 fine via GPS tracking."

        # --- DEFAULT FALLBACK ---
        else:
            reply = f"Hello <b>Venn</b>! 🚗 I'm your DriveGO AI. I can handle <b>Booking</b>, <b>IoT Controls</b>, or <b>Fleet Management</b>. How can I help?"

        # Database Storage
        try:
            ChatMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                message=user_message,
                response=reply
            )
        except Exception as e:
            print(f"Error: {e}")

        return JsonResponse({'response': reply})

    return render(request, 'chat.html')































# Change this:
    return render(request, 'chat.html')

# To this:
    return render(request, 'chat.html')

from .models import ParkingLocation
from django.http import JsonResponse

def api_parking_locations(request):
    from django.db.models import Q
    city = request.GET.get('city')
    if city:
        # Try to match city or specific hub name
        locations = ParkingLocation.objects.filter(Q(city__iexact=city) | Q(name__iexact=city))
        # If we matched a hub name but no city, try to get all hubs in that city
        if locations.exists() and not ParkingLocation.objects.filter(city__iexact=city).exists():
            hub = locations.first()
            locations = ParkingLocation.objects.filter(city__iexact=hub.city)
    else:
        locations = ParkingLocation.objects.all()
    
    data = []
    for loc in locations:
        data.append({
            'id': loc.id,
            'name': loc.name,
            'city': loc.city,
            'latitude': loc.latitude,
            'longitude': loc.longitude
        })
    return JsonResponse({'locations': data})

from .models.Booking import CancellationRequest
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cancel_booking_request(request, booking_id):
    if request.method == 'POST':
        try:
            booking = Booking.objects.get(id=booking_id)
            data = json.loads(request.body)
            reason = data.get('reason')
            issue = data.get('issue', '')
            
            cancel_req, created = CancellationRequest.objects.update_or_create(
                booking=booking,
                defaults={'reason': reason, 'issue': issue, 'status': 'Pending'}
            )
            return JsonResponse({'status': 'success', 'message': 'Cancellation request sent to admin.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
