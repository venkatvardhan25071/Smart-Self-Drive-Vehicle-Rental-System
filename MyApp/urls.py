from django.urls import path
from . import views  # use relative import for your app views


from django.contrib import admin










urlpatterns = [
    
   
   
    path('', views.index, name='index'),
    path('bbase/', views.bbase, name='bbase'),
    
    path('car-listing/', views.car_listing, name='car-listing'),
   

    path('Services/', views.Services, name='Services'),
    path('activity/', views.activity, name='activity'),
    path('account/', views.account, name='account'),
    path('booking-summary/', views.booking_summary, name='booking-summary'),
    path('vehicle-details/', views.vehicle_details, name='vehicle-details'),
    path('booking-success/', views.booking_success, name='booking-success'),
    path('bill/', views.bill, name='bill'),
      
    path('confirm/', views.confirm, name='confirm'),
    path('host/', views.host, name='host'),
    path('membership/', views.membership, name='membership'),
    path('contact/', views.contact, name='contact'),
    path('signin/', views.signin, name='signin'),
   
    path('vehicles/', views.vehicles, name='vehicles'),
    path('help/', views.help, name='help'),
    path('support/', views.support, name='support'),
    path('host/', views.host_vehicle, name='host'),
    path('support/email/', views.support_email, name='support_email'),
    path('support/call/', views.support_call, name='support_call'),
    path('support/report/', views.report_issue, name='report_issue'),

    path('settings/', views.settings, name='settings'),
    path('profile/', views.profile, name='profile'),
    
    
    
    path("Login/", views.Login, name="Login"),
    path("lock/", views.lock, name="lock"),
    path("key/", views.key, name="key"),
   
    path("thankyou/", views.thankyou, name="thankyou"),
    
    path('offers/', views.offers, name='offers'),
    
    path('changepassword/', views.changepassword, name='changepassword'),
    path('logout/', views.logout_user, name='logout'),

    path('signup/', views.signup, name='signup'),
    
     path('luxury/', views.luxury, name='luxury'),
    path('bikes/', views.bikes, name='bikes'),
    path('scooters/', views.scooters, name='scooters'),
    
    
   
    
    # Map the redirect URL to the thank you page view
    path('booking/thankyou/', views.thankyou_page, name='thankyou_page'),
    
    path('payment/', views.payment_view, name='payment'),
    # You also need a URL for the 'thankyou' page:
    path('thankyou/', views.thankyou_page, name='thankyou'),
    path('booking-summary/<int:vehicle_id>/', views.booking_summary, name='booking-summary'),
    
    path('payment/', views.payment_view, name='payment'), # Your payment page
    path('create-stripe-session/', views.create_stripe_session, name='create_session'),
    path('success/', views.success_view, name='success'), # IMPORTANT
   
   
    path('booking/submit/', views.process_booking, name='thankyou'),

# To this:
     path('booking/submit/', views.order, name='thankyou'),
     
     path('chat/', views.chat_view, name='chat'),
     path('location-tracking/', views.location_tracking, name='location-tracking'),
     path('location-signals-api/', views.location_signals_api, name='location-signals-api'),
     path('api/parking-locations/', views.api_parking_locations, name='api-parking-locations'),
     path('cancel-booking/<int:booking_id>/', views.cancel_booking_request, name='cancel_booking'),
]


    

