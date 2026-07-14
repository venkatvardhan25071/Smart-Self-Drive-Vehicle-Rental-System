import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicles.settings')
django.setup()

from MyApp.models import ParkingLocation

cities_data = {
    "Bengaluru": [12.9716, 77.5946],
    "Mysuru": [12.2958, 76.6394],
    "Mangaluru": [12.9141, 74.8560],
    "Hubballi": [15.3647, 75.1240],
    "Belagavi": [15.8497, 74.4977],
    "Mumbai": [19.0760, 72.8777],
    "Pune": [18.5204, 73.8567],
    "Nagpur": [21.1458, 79.0882],
    "Nashik": [19.9975, 73.7898],
    "Aurangabad": [19.8762, 75.3433],
    "Chennai": [13.0827, 80.2707],
    "Coimbatore": [11.0168, 76.9558],
    "Madurai": [9.9252, 78.1198],
    "Tiruchirappalli": [10.7905, 78.7047],
    "Salem": [11.6643, 78.1460],
    "Hyderabad": [17.3850, 78.4867],
    "Warangal": [17.9821, 79.5971],
    "Nizamabad": [18.6704, 78.0936],
    "Lucknow": [26.8467, 80.9462],
    "Kanpur": [26.4499, 80.3319],
    "Varanasi": [25.3176, 82.9739],
    "Agra": [27.1767, 78.0081],
    "Prayagraj": [25.4358, 81.8463],
    "Jaipur": [26.9124, 75.7873],
    "Jodhpur": [26.2389, 73.0243],
    "Udaipur": [24.5854, 73.7125],
    "Kota": [25.2138, 75.8648],
    "Ahmedabad": [23.0225, 72.5714],
    "Surat": [21.1702, 72.8311],
    "Vadodara": [22.3072, 73.1812],
    "Rajkot": [22.3039, 70.8022],
    "Kolkata": [22.5726, 88.3639],
    "Howrah": [22.5958, 88.3110],
    "Durgapur": [23.5204, 87.3119],
    "Kochi": [9.9312, 76.2673],
    "Thiruvananthapuram": [8.5241, 76.9366],
    "Kozhikode": [11.2588, 75.7804],
    "New Delhi": [28.6139, 77.2090],
    "Bangalore": [12.9716, 77.5946],
    "Goa": [15.2993, 74.1240],
    "Delhi": [28.7041, 77.1025],
    "Bellary": [15.1394, 76.9214],
    "Gangavathi": [15.4319, 76.5315],
    "Pondicherry": [11.9416, 79.8083],
    "Ladakh": [34.1526, 77.5771],
    "Patna": [25.5941, 85.1376],  # Bihar representation
    "Gaya": [24.7914, 85.0002],   # Bihar representation
    "Shimla": [31.1048, 77.1734],
    "Manali": [32.2396, 77.1887],
    "Dharamshala": [32.2190, 76.3234],
    "Haridwar": [29.9457, 78.1642],
    "Ranchi": [23.3441, 85.3096],
    "Indore": [22.7196, 75.8577],
    "Gwalior": [26.2183, 78.1828],
    "Jabalpur": [23.1815, 79.9864],
    "Ujjain": [23.1765, 75.7885],
    "Amritsar": [31.6340, 74.8723],
    "Visakhapatnam": [17.6868, 83.2185],
    "Vijayawada": [16.5062, 80.6480],
    "Guntur": [16.3067, 80.4365],
    "Nellore": [14.4426, 79.9865],
    "Kurnool": [15.8281, 78.0373],
    "Rajahmundry": [17.0005, 81.8040]
}

print("Adding dummy data...")

for city, coords in cities_data.items():
    # Primary Hub
    loc1, created1 = ParkingLocation.objects.get_or_create(
        city=city,
        name=f"{city} Central Hub",
        defaults={"latitude": coords[0], "longitude": coords[1]}
    )
    
    # Secondary Hub (offset slightly)
    loc2, created2 = ParkingLocation.objects.get_or_create(
        city=city,
        name=f"{city} Regional Pickup",
        defaults={"latitude": coords[0] + 0.02, "longitude": coords[1] + 0.02}
    )

print("Mass data loading complete. All states and cities added successfully!")
