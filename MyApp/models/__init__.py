from .vehicle import Vehicle

from .proxy_models import LuxuryVehicle,Bike,Scooter
# MyApp/models/__init__.py (Example if the file is named rentals.py)

# Change this: from .booking import CarBooking
# To this:
from .bill import CarBooking


from .category import Category
from .customer import Customer
from .Booking import Booking 
from .cars import Car
from .category import Category
from  .contact import  Contact
from  .orders import  Order
from .location_tracking import RentalHub, VehicleAvailabilitySignal, ParkingLocation
from .SupportTicket import SupportTicket
from .HostVehicle import HostVehicle
from .user_profile import UserProfile