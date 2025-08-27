# Drone Racing Service

A Django web application for managing drone racing competitions, pilots, drones, manufacturers, and race tracks.

## Project Structure

```
drone-racing-service/
├── accounts/         # Pilot authentication and user management
├── racing/           # Core racing models (Drones, Manufacturers, Race Tracks)
├── config/           # Django project configuration
├── templates/        # HTML templates with Bootstrap styling
└── manage.py         # Django management script
```

### Data Models

#### Pilot (Custom User)
- Username, email, password (inherited from AbstractUser)
- Drone license (unique 8-character identifier)
- Skill rating (integer, default: 1)
- Certification date (optional)

#### Drone
- Model name and specifications (max speed, weight)
- Manufacturer relationship
- Many-to-many relationship with pilots
- Unique constraint on model name + manufacturer

#### Manufacturer
- Company name and country
- Related drones catalog

#### Race Track
- Track name and location
- Difficulty levels: Beginner (1) to Professional (5)
- Track length in meters
- Optional record time tracking