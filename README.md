# Spices Backend - F1Soft Assessment

## Overview
This project is a part of assessment for **Backend Engineer Position**, implementing APIs for Users, Connections, and Notifications.
Built with **Django REST Framework** having **JWT authentication**, with **Celery** for asynchronous notifications.

---

## Features Implemented

### Users App
- User Registration
- JWT-based login (15 min expiry for access token, refresh token support)


### Connections App
- Send connection request
- Accept / Reject connection requests
- Search users using their name, company name, email or contact number
- Send a notification asynchronously when a connection request is accepted or rejected (Celery implementation for hanling asynchronous tasks.)

### Notifications App
- Manage notifications related to connection requests.

### Additional
- Unit tests for all major endpoints
- Postman coverage with sample requests

---

## Tech Stack
- **Python** 3.x
- **Django** 5.x
- **Django REST Framework**
- **SimpleJWT** for authentication
- **Celery** with Redis
- **SQLite** database

---

## Setup Instructions

```bash
# Clone repository
git clone https://github.com/PalRhitika/spices-backend.git
cd spices-backend

# Create virtual environment
python -m venv env
env\Scripts\activate   # linux: source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# For Admin Panel
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## Celery Setup

```bash
celery -A spices worker -l info
```

Make sure Redis is running before starting Celery.

---



## Environment Variables (.env.example)

```
# Django secret key (keep this secret in real .env)
DJANGO_SECRET_KEY=your-secret-key-here

# Debug mode (True for dev, False for prod)
DJANGO_DEBUG=True

# Allowed hosts (comma separated)
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database URL (you can switch to postgres/mysql by using dj-database-url)
DATABASE_URL=sqlite:///db.sqlite3

# Redis URL for Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

## Postman Collection
Import `sample-requests.json` into Postman to test all endpoints.
Or find the postman doumentation here:
https://documenter.getpostman.com/view/26667485/2sB3BEmphW
---

## API Endpoints

### **Users**
- `POST /users/register/` – Register a new user
- `POST /users/login/` – Login and get JWT tokens
- `POST /users/token/refresh/` – Refresh access token

### **Connections**
- `POST /connections/send/` – Send connection request
- `POST /connections/respond/{id}/` – Accept/Reject connection
- `GET /connections/sent/` – List sent requests
- `GET /connections/requests/` – List received requests

### **Notifications**
- `GET /api/notifications/` – List notifications
- `POST /api/notifications/` – Create notification
- `PATCH /api/notifications/{id}/` – Mark as read
- `DELETE /api/notifications/{id}/` – Delete notification

---
## Running Tests

```bash
python manage.py test
```

---

## Test Results
Example output from `python manage.py test`:
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.Bob
........
----------------------------------------------------------------------Ran 9 tests in 18.733s

OK
Destroying test database for alias 'default'...

```

---

---
## Security Best Practices Implemented
- Environment Variables – All sensitive data (secret key, DB credentials, Redis URL) is stored in .env and not committed to version control.

- Password Hashing – Uses Django’s built-in set_password() to securely hash passwords before storing them in the database.

- JWT Expiry & Refresh Tokens – Access tokens expire in 15 minutes to reduce risk from token theft, with refresh tokens for re-authentication.

- Field Validation – Email format, unique constraints, and Nepali contact number regex validation applied.

- Permission Classes – DRF’s IsAuthenticated enforced on all non-public endpoints.

- CSRF & CORS – CSRF enabled for session authentication and CORS settings can be restricted for production.

- Database Indexing – Optimized lookups with indexed fields for faster queries.

- Error Handling – Structured error responses to avoid exposing stack traces in production.
--

## Author
Rhitika Pal
