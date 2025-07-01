# Django Booking System API

## Project Setup

1. **Clone the repository** (if not already):
   ```bash
   git clone <your-repo-url>
   cd book-system
   ```
2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## API Documentation
- Swagger UI: [http://localhost:8000/api/docs/]
- Redoc: [http://localhost:8000/api/redoc/]

## Authentication
- Obtain JWT token: `POST /api/token/` with payload:
  ```json
  {
    "username": "<your_username>",
    "password": "<your_password>"
  }
  ```
- Use the access token in the `Authorization: Bearer <token>` header for authenticated endpoints.

## API Endpoints & Example Payloads

### 1. Set Weekly Availability (Authenticated)
- **Endpoint:** `POST /api/availability/`
- **Description:** Set a user's available time slot for a specific day of the week. To represent breaks, create multiple entries for the same day with different time ranges.
- **Payload:**
  ```json
  {
    "day_of_week": 0,           // 0=Monday, 1=Tuesday, ... 6=Sunday
    "start_time": "09:00",
    "end_time": "12:00"
  }
  ```

### 2. List User Availability (Authenticated)
- **Endpoint:** `GET /api/availability/`
- **Description:** Get all availability slots for the authenticated user.

### 3. Update Availability (Authenticated)
- **Endpoint:** `PUT /api/availability/{id}/`
- **Description:** Update a specific availability slot by its ID.
- **Payload:**
  ```json
  {
    "day_of_week": 0,
    "start_time": "10:00",
    "end_time": "13:00"
  }
  ```

### 4. Delete Availability (Authenticated)
- **Endpoint:** `DELETE /api/availability/{id}/`
- **Description:** Delete a specific availability slot by its ID.

### 5. List Available Booking Slots (Public)
- **Endpoint:** `GET /api/booking/available_slots/?user_id=<id>&date=<YYYY-MM-DD>`
- **Description:** Get all available time slots for a user on a specific date, considering their availability and existing bookings.
- **Example:**
  ```
  /api/booking/available_slots/?user_id=1&date=2025-07-07
  ```
- **Response:**
  ```json
  [
    {"start_time": "09:30:00", "end_time": "10:00:00", "duration": 30},
    ...
  ]
  ```

### 6. Book a Slot (Guest)
- **Endpoint:** `POST /api/booking/`
- **Description:** Book a time slot with a user. Bookings must not overlap and must fit within the user's availability.
- **Payload:**
  ```json
  {
    "user": 1,  // ID of the user being booked
    "date": "2025-07-07",
    "start_time": "10:00",
    "end_time": "10:30",
    "guest_name": "Alice",
    "guest_email": "alice@example.com"
  }
  ```

### 7. List Bookings for a User (Public)
- **Endpoint:** `GET /api/booking/?user_id=<id>`
- **Description:** List all bookings for a specific user.

### 8. Update Booking (Guest)
- **Endpoint:** `PUT /api/booking/{id}/`
- **Description:** Update a specific booking by its ID. (Only allowed if your API permissions allow it.)
- **Payload:**
  ```json
  {
    "user": 1,
    "date": "2025-07-07",
    "start_time": "11:00",
    "end_time": "11:30",
    "guest_name": "Alice",
    "guest_email": "alice@example.com"
  }
  ```

### 9. Delete Booking (Guest)
- **Endpoint:** `DELETE /api/booking/{id}/`
- **Description:** Delete a specific booking by its ID. (Only allowed if your API permissions allow it.)

### 10. Obtain JWT Token
- **Endpoint:** `POST /api/token/`
- **Description:** Obtain JWT access and refresh tokens for authentication.
- **Payload:**
  ```json
  {
    "username": "<your_username>",
    "password": "<your_password>"
  }
  ```
- **Response:**
  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>"
  }
  ```

### 11. Refresh JWT Token
- **Endpoint:** `POST /api/token/refresh/`
- **Description:** Refresh your JWT access token using a refresh token.
- **Payload:**
  ```json
  {
    "refresh": "<refresh_token>"
  }
  ```
- **Response:**
  ```json
  {
    "access": "<new_access_token>"
  }
  ```

## Running Tests

To run the unit tests:

```bash
python manage.py test
```

## Notes
- Bookings must not overlap and must fit within the user's availability.
- Only authenticated users can set their own availability.
- Guests can view available slots and book them.
- All time fields use 24-hour format (`HH:MM` or `HH:MM:SS`).
- For detailed API schema and testing, use Swagger UI or Redoc.
