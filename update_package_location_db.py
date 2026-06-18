"""
Direct database update for DFX-2XWJFI8R package location to Islamabad, Pakistan
This script connects directly to the production database
"""
import psycopg2
from datetime import datetime
import os

# Database connection (you'll need to provide the DATABASE_URL)
print("=" * 70)
print("📦 PACKAGE LOCATION UPDATE - DFX-2XWJFI8R")
print("=" * 70)
print("\nThis script will update the package location to Islamabad, Pakistan")
print("\nYou'll need your DATABASE_URL from your deployment (Render/Railway)")
print("Format: postgresql://user:password@host:port/database")
print("\nOr provide individual connection details:\n")

# Get database connection details
db_url = input("Enter DATABASE_URL (or press Enter to input individual details): ").strip()

if db_url:
    # Parse DATABASE_URL
    conn = psycopg2.connect(db_url)
else:
    host = input("Database Host: ").strip()
    port = input("Database Port (default 5432): ").strip() or "5432"
    database = input("Database Name: ").strip()
    user = input("Database User: ").strip()
    password = input("Database Password: ").strip()
    
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

cursor = conn.cursor()
print("\n✅ Connected to database successfully!\n")

# Package details
tracking_number = 'DFX-2XWJFI8R'

# Check if package exists
cursor.execute("""
    SELECT id, tracking_number, status, sender_city, sender_country, 
           receiver_city, receiver_country
    FROM packages_package
    WHERE tracking_number = %s
""", (tracking_number,))

package = cursor.fetchone()

if not package:
    print(f"❌ Package {tracking_number} not found!")
    conn.close()
    exit(1)

package_id = package[0]
print(f"📦 Package Found: {package[1]}")
print(f"   Status: {package[2]}")
print(f"   Route: {package[3]}, {package[4]} → {package[5]}, {package[6]}")

# Get current location
cursor.execute("""
    SELECT location, timestamp
    FROM tracking_trackinghistory
    WHERE package_id = %s
    ORDER BY timestamp DESC
    LIMIT 1
""", (package_id,))

current_location = cursor.fetchone()
if current_location:
    print(f"   Current Location: {current_location[0]}")
    print(f"   Last Update: {current_location[1]}")

# New location details
new_location = "Islamabad, Pakistan"
new_lat = 33.6844
new_lng = 73.0479
timestamp = datetime.now()

print(f"\n🔄 Updating to: {new_location}")
print(f"   Coordinates: ({new_lat}, {new_lng})")
print(f"   Timestamp: {timestamp}")

# Confirm update
confirm = input("\n⚠️  Proceed with update? (yes/no): ").strip().lower()

if confirm != 'yes':
    print("❌ Update cancelled")
    conn.close()
    exit(0)

# Insert new tracking history entry
cursor.execute("""
    INSERT INTO tracking_trackinghistory 
    (package_id, status, location, latitude, longitude, notes, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id
""", (
    package_id,
    "In Transit",
    new_location,
    new_lat,
    new_lng,
    f"Package arrived in {new_location}",
    timestamp
))

tracking_id = cursor.fetchone()[0]

# Update package status to in_transit (if not already)
cursor.execute("""
    UPDATE packages_package
    SET status = 'in_transit'
    WHERE id = %s
""", (package_id,))

# Commit changes
conn.commit()

print(f"\n✅ Location updated successfully!")
print(f"   New Tracking Entry ID: {tracking_id}")
print(f"   Timestamp: {timestamp.strftime('%b %d, %Y at %I:%M %p')}")

# Calculate distance to Lahore
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return 6371 * c

lahore_lat, lahore_lng = 31.5497, 74.3436
dist = haversine(new_lat, new_lng, lahore_lat, lahore_lng)
hours = dist / 65

print(f"\n📏 Distance to destination (Lahore): {dist:.1f} km")
print(f"⏱️  Estimated delivery time: {hours:.1f} hours")

print(f"\n🗺️  Track online:")
print(f"   https://dailyfx-delivery.onrender.com/track/?q={tracking_number}")

# Close connection
cursor.close()
conn.close()

print("\n" + "=" * 70)
print("✅ DATABASE UPDATE COMPLETE")
print("=" * 70)
