"""
Update DFX-2XWJFI8R package location to Islamabad, Pakistan
"""
import os
import sys

# Get the repository path
repo_path = input("Enter the full path to your consignment-site repository: ").strip()

if not os.path.exists(repo_path):
    print(f"❌ Path not found: {repo_path}")
    sys.exit(1)

sys.path.insert(0, repo_path)
os.chdir(repo_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'consignment.settings')

import django
django.setup()

from packages.models import Package
from tracking.models import TrackingHistory
from django.utils import timezone

print("=" * 70)
print("📦 UPDATING PACKAGE LOCATION")
print("=" * 70)

# Find the package
tracking_number = 'DFX-2XWJFI8R'
package = Package.objects.filter(tracking_number=tracking_number).first()

if not package:
    print(f"❌ Package {tracking_number} not found!")
    sys.exit(1)

print(f"\n📦 Package: {package.tracking_number}")
print(f"   Status: {package.status}")
print(f"   Route: {package.sender_city}, {package.sender_country} → {package.receiver_city}, {package.receiver_country}")

# Get current location
last_tracking = package.tracking_history.order_by('-timestamp').first()
if last_tracking:
    print(f"   Current Location: {last_tracking.location}")
    print(f"   Last Update: {last_tracking.timestamp.strftime('%b %d, %Y at %I:%M %p')}")

# New location: Islamabad, Pakistan
new_city = "Islamabad"
new_country = "Pakistan"
new_location = f"{new_city}, {new_country}"
new_lat = 33.6844
new_lng = 73.0479

print(f"\n🔄 Updating to: {new_location}")
print(f"   Coordinates: ({new_lat}, {new_lng})")

# Create new tracking entry
tracking = TrackingHistory.objects.create(
    package=package,
    status="In Transit",
    location=new_location,
    latitude=new_lat,
    longitude=new_lng,
    notes=f"Package arrived in {new_location}",
    timestamp=timezone.now()
)

# Ensure package status is in_transit
package.status = 'in_transit'
package.save()

print(f"\n✅ Location updated successfully!")
print(f"   Tracking Entry ID: {tracking.id}")
print(f"   Timestamp: {tracking.timestamp.strftime('%b %d, %Y at %I:%M %p')}")

# Calculate distance to destination (Lahore)
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c

# Lahore coordinates
lahore_lat, lahore_lng = 31.5497, 74.3436
dist = haversine(new_lat, new_lng, lahore_lat, lahore_lng)
hours = dist / 65  # Average speed 65 km/h

print(f"\n📏 Distance to destination ({package.receiver_city}): {dist:.1f} km")
print(f"⏱️  Estimated delivery time: {hours:.1f} hours")

print(f"\n🗺️  Track online:")
print(f"   https://dailyfx-delivery.onrender.com/track/?q={tracking_number}")

print("\n" + "=" * 70)
print("✅ PACKAGE LOCATION UPDATE COMPLETE")
print("=" * 70)
