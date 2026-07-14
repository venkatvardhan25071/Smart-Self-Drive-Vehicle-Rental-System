# from email.mime import message
# from pyexpat import model
from django.http import Http404, HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from psycopg.pq import error_message
import re


from .models import CarBooking # Import your model

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Booking



import stripe
from django.conf import settings









from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


from .models.cars import Car
from .models.orders import Order
from .models.category import Category

from .models.customer import Customer
from .models.contact import Contact



from django.shortcuts import render
from .models.vehicle import Vehicle




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



       



        messages.success(request, "Account created successfully. Please log in.")

        return redirect('signin')  # adjust to your login route name



    # GET request => show signup form

    return render(request, 'signup.html') 

        
        
        
     
     
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


    
    
    
    
  

def changepassword(request):
    return render(request, 'changepassword.html')  
    
    
    
def payment(request):
    return render(request, 'payment.html')     


def offers(request):
    return render(request, 'offers.html')     
     
     
     
     
     
def Login(request):
    return render(request, 'login.html')     
     
     
     
def host(request):
    return render(request, 'host.html')


     
def Services(request):
    return render(request, 'Services.html')
     
     
     


def bbase(request):
	return render(request,'bbase.html')


def car_listing(request):
    return render(request,'car-listing.html')



def activity(request):
    return render(request,'activity.html')

def account(request):
    return render(request,'account.html')

def vehicle_details(request):
    return render(request,'vehicle-details.html')

def booking_summary(request):
    return render(request,'booking-summary.html')

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

def profile(request):
    return render(request, 'profile.html')

def help(request):
    return render(request, 'help.html')

def thankyou(request):
    return render(request, 'thankyou.html')



def confirm(request):
    return render(request,'confirm.html')















# Set your secret key
stripe.api_key = "your_stripe_secret_key_here"

@csrf_exempt
def create_stripe_session(request):
    if request.method == 'POST':
        try:
            # 1. Grab Files and Text Data from Multipart Form
            aadhaar = request.FILES.get('aadhaar')
            dl = request.FILES.get('dl')
            
            # 2. Save Data to Database first (as unpaid)
            booking = Booking.objects.create(
                vehicle_name=request.POST.get('vname'),
                full_name=request.POST.get('name'),
                phone=request.POST.get('phone'),
                email=request.POST.get('email'),
                location=request.POST.get('location'),
                color=request.POST.get('color'),
                pickup_date=request.POST.get('pickup'),
                return_date=request.POST.get('return'),
                total_amount=request.POST.get('total'),
                aadhaar_card=aadhaar,
                driving_license=dl
            )

            # 3. Create Stripe Checkout Session
            # Multiply by 100 because Stripe works in paise/cents
            unit_amount = int(float(request.POST.get('total')) * 100)

            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {'name': f"Booking for {booking.vehicle_name}"},
                        'unit_amount': unit_amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/payment/'),
                client_reference_id=str(booking.id),
            )

            return JsonResponse({'id': session.id})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'message': 'Invalid request'}, status=405)