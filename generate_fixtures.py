#!/usr/bin/env python
"""
Script to generate random data fixtures for the drone racing service.
Run this script to create a fixtures.json file that can be loaded with:
python manage.py loaddata fixtures.json
"""

import json
import random
import string
from datetime import date, timedelta, datetime, timezone
from faker import Faker

fake = Faker()

def generate_drone_license():
    """Generate a random 8-character drone license (uppercase letters and numbers)"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_manufacturers(count=10):
    """Generate manufacturer data"""
    manufacturers = []
    countries = ['USA', 'Germany', 'Japan', 'China', 'France', 'Italy', 'UK', 'Canada', 'Australia', 'South Korea']
    company_names = [
        'AeroTech', 'SkyDrone', 'RacingWings', 'VelocityDrones', 'TurboFly',
        'SpeedCraft', 'AirRacer', 'DroneMax', 'FlightForce', 'RapidRotor',
        'PropellerPro', 'AeroSpeed', 'SkyRocket', 'DroneElite', 'AirVelocity'
    ]
    used_names = set()
    
    for i in range(count):
        while True:
            name = random.choice(company_names) + f" {random.choice(['Industries', 'Corp', 'Ltd', 'Systems', 'Tech'])}"
            if name not in used_names:
                used_names.add(name)
                break
        
        manufacturers.append({
            "model": "racing.manufacturer",
            "pk": i + 1,
            "fields": {
                "name": name,
                "country": random.choice(countries)
            }
        })
    
    return manufacturers

def generate_pilots(count=20):
    """Generate pilot data"""
    pilots = []
    used_licenses = set()
    used_usernames = set()
    
    for i in range(count):
        # Generate unique drone license
        while True:
            license_num = generate_drone_license()
            if license_num not in used_licenses:
                used_licenses.add(license_num)
                break
        
        # Generate unique username
        while True:
            username = fake.user_name()
            if username not in used_usernames:
                used_usernames.add(username)
                break
        
        # Random certification date (within last 5 years or None)
        cert_date = None
        if random.choice([True, False]):  # 50% chance of having certification
            cert_date = fake.date_between(start_date=date.today() - timedelta(days=1825), end_date=date.today()).isoformat()
        
        pilots.append({
            "model": "accounts.pilot",
            "pk": i + 1,
            "fields": {
                "username": username,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email(),
                "is_staff": False,
                "is_active": True,
                "is_superuser": False,
                "date_joined": fake.date_time_between(start_date=datetime(2020, 1, 1, tzinfo=timezone.utc)).isoformat(),
                "drone_license": license_num,
                "skill_rating": random.randint(1, 100),
                "certification_date": cert_date,
                "password": "pbkdf2_sha256$600000$dummy$dummy"  # Dummy password hash
            }
        })
    
    return pilots

def generate_drones(count=30, manufacturer_count=10):
    """Generate drone data"""
    drones = []
    drone_models = [
        'Phantom', 'Mavic', 'Inspire', 'Spark', 'Mini', 'Air', 'Pro', 'Elite',
        'Racer', 'Speed', 'Velocity', 'Thunder', 'Lightning', 'Storm', 'Blitz',
        'Falcon', 'Eagle', 'Hawk', 'Swift', 'Arrow', 'Bullet', 'Rocket'
    ]
    
    for i in range(count):
        model_name = f"{random.choice(drone_models)} {random.choice(['X', 'Pro', 'Elite', 'Racing', 'Speed'])}{random.randint(100, 999)}"
        
        drones.append({
            "model": "racing.drone",
            "pk": i + 1,
            "fields": {
                "model_name": model_name,
                "max_speed": round(random.uniform(50.0, 200.0), 1),  # 50-200 km/h
                "weight": str(round(random.uniform(0.5, 5.0), 2)),  # 0.5-5.0 kg
                "manufacturer": random.randint(1, manufacturer_count),
                "pilots": random.sample(range(1, 21), random.randint(0, 3))  # 0-3 pilots per drone
            }
        })
    
    return drones

def generate_racetracks(count=15):
    """Generate racetrack data"""
    racetracks = []
    track_names = [
        'Thunder Valley Circuit', 'Sky Harbor Track', 'Velocity Speedway', 'Aerial Arena',
        'Cloud Nine Circuit', 'Lightning Loop', 'Storm Ridge Track', 'Wind Tunnel Raceway',
        'Turbulence Track', 'Stratosphere Speedway', 'Jetstream Circuit', 'Altitude Arena',
        'Supersonic Speedway', 'Mach One Track', 'Hypersonic Highway', 'Tornado Alley Track',
        'Hurricane Harbor', 'Cyclone Circuit', 'Blizzard Boulevard', 'Meteor Speedway'
    ]
    
    locations = [
        'Las Vegas, Nevada', 'Miami, Florida', 'Austin, Texas', 'Los Angeles, California',
        'New York, New York', 'Chicago, Illinois', 'Phoenix, Arizona', 'Denver, Colorado',
        'Seattle, Washington', 'Atlanta, Georgia', 'Boston, Massachusetts', 'Portland, Oregon',
        'San Francisco, California', 'Dallas, Texas', 'Detroit, Michigan'
    ]
    
    used_names = set()
    
    for i in range(count):
        # Ensure unique track names
        while True:
            name = random.choice(track_names)
            if name not in used_names:
                used_names.add(name)
                break
        
        # Generate record time (between 30 seconds and 5 minutes)
        record_seconds = random.randint(30, 300)
        record_time = f"00:{record_seconds // 60:02d}:{record_seconds % 60:02d}"
        
        racetracks.append({
            "model": "racing.racetrack",
            "pk": i + 1,
            "fields": {
                "name": name,
                "difficulty_level": random.randint(1, 5),
                "length_meters": random.randint(500, 3000),
                "location": random.choice(locations),
                "record_time": record_time if random.choice([True, False]) else None  # 50% chance of having record
            }
        })
    
    return racetracks

def main():
    """Generate all fixtures and save to JSON file"""
    print("Generating random data fixtures...")
    
    fixtures = []
    
    # Generate data
    print("- Generating manufacturers...")
    fixtures.extend(generate_manufacturers(10))
    
    print("- Generating pilots...")
    fixtures.extend(generate_pilots(20))
    
    print("- Generating drones...")
    fixtures.extend(generate_drones(30, 10))
    
    print("- Generating racetracks...")
    fixtures.extend(generate_racetracks(15))
    
    # Save to JSON file
    output_file = 'fixtures.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixtures, f, indent=2, ensure_ascii=False)
    
    print(f"\nFixtures generated successfully!")
    print(f"Total records: {len(fixtures)}")
    print(f"Saved to: {output_file}")
    print(f"\nTo load the data into your database, run:")
    print(f"python manage.py loaddata {output_file}")

if __name__ == "__main__":
    main()
