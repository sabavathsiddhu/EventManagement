# 🔌 API Documentation - Smart Campus Event Management System

**Complete endpoint reference for all routes in the application.**

---

## 📌 API Overview

| Property | Value |
|----------|-------|
| **Base URL** | http://localhost:5000 (development) |
| **API Version** | 1.0 |
| **Authentication** | Session-based (Flask sessions) |
| **Content-Type** | application/json, application/x-www-form-urlencoded |
| **Total Endpoints** | 27 routes |

---

## 🔑 Authentication

### Session-Based Authentication
All protected routes require a valid user session. Sessions are managed via Flask cookies.

```python
# Session attributes
session['student_id']        # For student users
session['admin_id']          # For admin users
session['organiser_id']      # For organiser users
session['user_type']         # 'student', 'admin', or 'organiser'
session['user_name']         # User's full name
session['last_activity']     # Last activity timestamp
```

### Login Decorator Usage
```python
@login_required('student')   # Requires student session
@login_required('admin')     # Requires admin session
@login_required('organiser') # Requires organiser session
```

### Session Timeout
- Default timeout: **3600 seconds** (1 hour)
- Configurable via `config.SESSION_TIMEOUT`
- Auto-logout on inactivity

---

## 🌐 Endpoints

### Authentication Routes (3 endpoints)

#### 1. Login
```
Route:   POST /auth/login
Type:    POST
Auth:    None
Returns: Redirect (302) to dashboard or error page
```

**Parameters (Form Data):**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "user_type": "student|admin|organiser"
}
```

**Response:**
- Success: Redirect to `/student/dashboard` or similar
- Failure: Render login template with error message

**Example:**
```bash
curl -X POST http://localhost:5000/auth/login \
  -d "email=student@campus.edu&password=pass123&user_type=student"
```

---

#### 2. Student Registration
```
Route:   GET /auth/register/student
Route:   POST /auth/register/student
Type:    GET (form), POST (submission)
Auth:    None
Returns: HTML form (GET) or Redirect (POST)
```

**GET Parameters:** None

**POST Parameters (Form Data):**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePass123",
  "confirmation_password": "securePass123",
  "enrollment_number": "E2023001",
  "cgpa": "8.5",
  "attendance": "85",
  "phone": "9876543210"
}
```

**Response:**
- Success: Redirect to `/auth/login` with success message
- Failure: Render registration form with error messages

---

#### 3. Organiser Registration
```
Route:   GET /auth/register/organiser
Route:   POST /auth/register/organiser
Type:    GET (form), POST (submission)
Auth:    None
Returns: HTML form (GET) or Redirect (POST)
```

**POST Parameters (Form Data):**
```json
{
  "name": "Dr. Jane Smith",
  "email": "jane@campus.edu",
  "password": "securePass123",
  "confirmation_password": "securePass123",
  "phone": "9876543210",
  "department": "Computer Science"
}
```

---

### Student Routes (8 endpoints)

#### 1. Student Dashboard
```
Route:   GET /student/dashboard
Auth:    Required (student)
Returns: HTML template
```

**Response Data:**
```json
{
  "student_cgpa": 8.5,
  "student_attendance": 85,
  "registered_events": 5,
  "certificates_count": 3,
  "upcoming_events": [
    {
      "event_id": 1,
      "event_name": "Tech Summit 2024",
      "event_date": "2024-05-15",
      "min_cgpa": 7.0,
      "min_attendance": 80
    }
  ],
  "registered_events_list": [...]
}
```

**Example:**
```bash
curl -X GET http://localhost:5000/student/dashboard \
  -H "Cookie: session=your_session_id"
```

---

#### 2. Browse Events
```
Route:   GET /student/events
Auth:    Required (student)
Returns: HTML template
```

**Query Parameters:**
```
?page=1              # Pagination (optional)
?sort=date           # Sort by: date, name (optional)
&search=summit       # Search term (optional)
```

**Response Data:**
```json
{
  "events": [
    {
      "event_id": 1,
      "event_name": "Tech Summit 2024",
      "event_date": "2024-05-15",
      "event_description": "...",
      "min_cgpa": 7.0,
      "min_attendance": 80,
      "is_paid": true,
      "event_fee": 500,
      "is_eligible": true,
      "is_registered": false,
      "organiser_name": "Dr. Jane Smith"
    }
  ],
  "total_events": 15,
  "page": 1,
  "pages": 2
}
```

---

#### 3. Register for Event
```
Route:   POST /student/register/<event_id>
Auth:    Required (student)
Returns: JSON response
```

**URL Parameters:**
```
event_id: Integer (required)
```

**Response (JSON):**
```json
{
  "success": true,
  "message": "Successfully registered for event",
  "registration_id": 123,
  "requires_payment": false
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "You are not eligible for this event",
  "reasons": [
    "Your CGPA is below minimum requirement",
    "Your attendance is insufficient"
  ]
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/student/register/1 \
  -H "Cookie: session=your_session_id" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

#### 4. Payment Form
```
Route:   GET /student/payment/<registration_id>
Auth:    Required (student)
Returns: HTML template with payment form
```

**Response:** Razorpay payment form embedded in HTML

---

#### 5. Verify Payment
```
Route:   POST /student/payment/verify
Auth:    Required (student)
Returns: Redirect or JSON
```

**POST Parameters (Form Data):**
```json
{
  "razorpay_order_id": "order_xxxxx",
  "razorpay_payment_id": "pay_xxxxx",
  "razorpay_signature": "signature_xxxxx"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Payment verified successfully",
  "payment_id": 456
}
```

---

#### 6. View Certificates
```
Route:   GET /student/certificates
Auth:    Required (student)
Returns: HTML template
```

**Response Data:**
```json
{
  "certificates": [
    {
      "certificate_id": 1,
      "certificate_number": "CERT-2024-001",
      "event_name": "Tech Summit 2024",
      "issue_date": "2024-05-16",
      "certificate_file": "certificate_CERT-2024-001.pdf",
      "downloads": 2
    }
  ],
  "total_certificates": 3
}
```

---

#### 7. Download Certificate
```
Route:   GET /student/certificate/download/<certificate_id>
Auth:    Required (student)
Returns: Binary PDF file or redirect
```

**Response:** PDF file with appropriate headers

**Status Codes:**
- 200: File sent successfully
- 404: Certificate not found
- 403: Forbidden (not certificate owner)

---

#### 8. Student Profile
```
Route:   GET /student/profile
Route:   POST /student/profile
Auth:    Required (student)
Returns: HTML template (GET) or Redirect (POST)
```

**GET Response:**
```json
{
  "student_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "enrollment_number": "E2023001",
  "cgpa": 8.5,
  "attendance": 85,
  "phone": "9876543210"
}
```

**POST Parameters:**
```json
{
  "phone": "9876543211",
  "cgpa": "8.6",
  "attendance": "86"
}
```

---

### Admin Routes (9 endpoints)

#### 1. Admin Dashboard
```
Route:   GET /admin/dashboard
Auth:    Required (admin)
Returns: HTML template
```

**Response Data:**
```json
{
  "total_students": 250,
  "total_events": 15,
  "total_registrations": 850,
  "total_payments": 125000,
  "pending_certificates": 42,
  "recent_events": [...],
  "top_events": [...]
}
```

---

#### 2. List Events
```
Route:   GET /admin/events
Auth:    Required (admin)
Returns: HTML template
```

**Query Parameters:**
```
?page=1              # Pagination
?status=upcoming     # Filter: upcoming, ongoing, completed
?sort=date           # Sort field
&search=summit       # Search term
```

---

#### 3. Create Event
```
Route:   GET /admin/event/create
Route:   POST /admin/event/create
Auth:    Required (admin)
Returns: HTML form (GET) or Redirect (POST)
```

**POST Parameters:**
```json
{
  "event_name": "Tech Summit 2024",
  "event_date": "2024-05-15",
  "event_description": "Description here",
  "location": "Main Auditorium",
  "min_cgpa": 7.0,
  "min_attendance": 80,
  "is_paid": true,
  "event_fee": 500,
  "organiser_id": 1,
  "event_type": "technical"
}
```

**Response:** Redirect to event details or error

---

#### 4. Edit Event
```
Route:   GET /admin/event/<event_id>/edit
Route:   POST /admin/event/<event_id>/edit
Auth:    Required (admin)
Returns: HTML form (GET) or Redirect (POST)
```

**Response (GET):** Pre-filled form with event data

---

#### 5. Delete Event
```
Route:   POST /admin/event/<event_id>/delete
Auth:    Required (admin)
Returns: JSON or Redirect
```

**Response:**
```json
{
  "success": true,
  "message": "Event deleted successfully"
}
```

---

#### 6. View Registrations
```
Route:   GET /admin/registrations
Auth:    Required (admin)
Returns: HTML template
```

**Query Parameters:**
```
?page=1              # Pagination
?event_id=1          # Filter by event
?status=pending      # Filter by status
&search=john         # Search term
```

---

#### 7. List Students
```
Route:   GET /admin/students
Auth:    Required (admin)
Returns: HTML template
```

**Query Parameters:**
```
?page=1              # Pagination
?sort=name           # Sort field
&search=john         # Search term
```

---

#### 8. Analytics Dashboard
```
Route:   GET /admin/analytics
Auth:    Required (admin)
Returns: HTML template
```

**Response Data:**
```json
{
  "event_stats": {
    "total": 15,
    "active": 8,
    "completed": 7
  },
  "registration_stats": {
    "total": 850,
    "average_per_event": 56.67
  },
  "payment_stats": {
    "total_revenue": 125000,
    "success_rate": 95.5,
    "failed_payments": 6
  },
  "attendance_stats": {
    "average_attendance_rate": 87.3,
    "total_attendees": 742
  }
}
```

---

#### 9. List Organisers
```
Route:   GET /admin/organisers
Auth:    Required (admin)
Returns: HTML template
```

**Response Data:**
```json
{
  "organisers": [
    {
      "organiser_id": 1,
      "name": "Dr. Jane Smith",
      "email": "jane@campus.edu",
      "department": "Computer Science",
      "event_count": 5,
      "phone": "9876543210"
    }
  ],
  "total_organisers": 8
}
```

---

### Organiser Routes (7 endpoints)

#### 1. Organiser Dashboard
```
Route:   GET /organiser/dashboard
Auth:    Required (organiser)
Returns: HTML template
```

**Response Data:**
```json
{
  "total_events": 5,
  "upcoming_events": 2,
  "ongoing_events": 1,
  "completed_events": 2,
  "total_registrations": 150,
  "events": [...]
}
```

---

#### 2. Event Details
```
Route:   GET /organiser/event/<event_id>
Auth:    Required (organiser)
Returns: HTML template
```

**Response Data:**
```json
{
  "event_id": 1,
  "event_name": "Tech Summit 2024",
  "event_date": "2024-05-15",
  "event_description": "...",
  "location": "Main Auditorium",
  "total_registrations": 45,
  "students": [
    {
      "student_id": 1,
      "name": "John Doe",
      "email": "john@email.com",
      "cgpa": 8.5,
      "attendance_status": "pending",
      "certificate_generated": false
    }
  ]
}
```

---

#### 3. Mark Attendance (Form)
```
Route:   GET /organiser/attendance/<event_id>
Auth:    Required (organiser)
Returns: HTML template
```

**Response:** Attendance marking form with student list

---

#### 4. Save Attendance
```
Route:   POST /organiser/attendance/save
Auth:    Required (organiser)
Returns: JSON response
```

**POST Parameters (JSON):**
```json
{
  "event_id": 1,
  "attendances": [
    {
      "registration_id": 123,
      "student_id": 1,
      "status": "present",
      "check_in_time": "2024-05-15 10:00:00",
      "check_out_time": "2024-05-15 12:00:00"
    },
    {
      "registration_id": 124,
      "student_id": 2,
      "status": "absent",
      "check_in_time": null,
      "check_out_time": null
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Attendance saved successfully",
  "records_updated": 45
}
```

---

#### 5. Face Recognition Interface
```
Route:   GET /organiser/face-recognition/<event_id>
Auth:    Required (organiser)
Returns: HTML template with camera feed
```

**Features:**
- Live webcam feed
- Real-time face detection
- Automatic attendance marking
- Fallback manual entry

---

#### 6. View Certificate Eligibility
```
Route:   GET /organiser/certificates/<event_id>
Auth:    Required (organiser)
Returns: HTML template
```

**Response Data:**
```json
{
  "event_id": 1,
  "eligible_students": 42,
  "students": [
    {
      "registration_id": 123,
      "student_id": 1,
      "name": "John Doe",
      "attendance": "present",
      "certificate_generated": false
    }
  ]
}
```

---

#### 7. Generate Certificates
```
Route:   POST /organiser/certificates/generate
Auth:    Required (organiser)
Returns: JSON response
```

**POST Parameters (JSON):**
```json
{
  "event_id": 1,
  "student_ids": [1, 2, 3, 4, 5],
  "batch_mode": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Certificates generated successfully",
  "certificates_generated": 5,
  "certificate_numbers": [
    "CERT-2024-001",
    "CERT-2024-002",
    "CERT-2024-003",
    "CERT-2024-004",
    "CERT-2024-005"
  ]
}
```

---

## 🔄 Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK - Request successful | Event displayed successfully |
| 302 | Redirect - After form submission | Login redirect to dashboard |
| 400 | Bad Request - Invalid parameters | Missing required field |
| 401 | Unauthorized - No session | Accessing protected route without login |
| 403 | Forbidden - Access denied | Student accessing admin page |
| 404 | Not Found - Resource not found | Non-existent event ID |
| 500 | Server Error - Internal error | Database connection error |

---

## 🔒 Authentication Examples

### Login Flow
```
1. GET /auth/login              → Display login form
2. POST /auth/login             → Submit credentials
3. Server validates & creates session
4. Redirect to /student/dashboard (or admin/organiser)
```

### Protected Route Access
```
1. GET /student/dashboard
2. Server checks session
3. If valid → Display dashboard
4. If invalid → Redirect to login
```

---

## 📊 Response Examples

### Success Response (Student Registration)
```json
{
  "success": true,
  "message": "Successfully registered for event",
  "registration_id": 123,
  "requires_payment": true,
  "event_fee": 500
}
```

### Error Response (Eligibility Check Failed)
```json
{
  "success": false,
  "message": "Not eligible for this event",
  "reasons": [
    "CGPA 7.5 is below minimum requirement 8.0",
    "Attendance 75% is below minimum requirement 80%"
  ],
  "event_id": 1
}
```

### Payment Verification Response
```json
{
  "success": true,
  "payment_id": 456,
  "amount": 500,
  "status": "completed",
  "razorpay_payment_id": "pay_xxxxx",
  "timestamp": "2024-04-20 14:30:00"
}
```

---

## 🔌 API Integration Examples

### Using Python Requests
```python
import requests

# Login
response = requests.post('http://localhost:5000/auth/login', 
  data={
    'email': 'john@example.com',
    'password': 'password123',
    'user_type': 'student'
  }
)

# Get events (with session cookie)
response = requests.get('http://localhost:5000/student/events',
  cookies=response.cookies
)
```

### Using JavaScript Fetch
```javascript
// Register for event
fetch('/student/register/1', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include',
  body: JSON.stringify({})
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## 📝 API Pagination

### Query Parameters
```
?page=1              # Page number (1-indexed)
&per_page=10         # Items per page (optional)
&sort=date           # Sort field (optional)
&order=desc          # Sort order: asc, desc (optional)
```

### Paginated Response
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "pages": 10,
  "per_page": 10,
  "has_next": true,
  "has_prev": false
}
```

---

## 🔐 Rate Limiting

Current implementation: No rate limiting

**Future Enhancement**: Implement rate limiting
```
- 10 login attempts per minute per IP
- 100 API calls per minute per user
- 1000 API calls per day per user
```

---

## 📚 Webhook Integration

### Payment Webhook (Razorpay)
```
Event: payment.authorized
POST /webhook/razorpay

Payload:
{
  "event": "payment.authorized",
  "payload": {
    "payment": {
      "id": "pay_xxxxx",
      "amount": 50000,
      "currency": "INR",
      "status": "authorized"
    }
  }
}
```

---

## 🚀 API Versioning

Current API Version: **1.0**

Future versions may include:
- `/api/v2/` endpoints
- GraphQL API
- REST API improvements
- Webhook enhancements

---

## 📖 Error Handling

### Error Response Format
```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message",
  "details": {
    "field": "error_for_field"
  },
  "code": 400
}
```

---

## 💡 Best Practices

### For API Consumers
1. Always check `success` field first
2. Handle timeout errors gracefully
3. Implement retry logic for failed requests
4. Cache responses when appropriate
5. Validate data before submission

### For API Development
1. Validate all inputs
2. Sanitize database inputs
3. Log all API calls
4. Monitor API performance
5. Version your API

---

**API Documentation Version**: 1.0.0  
**Last Updated**: April 2024  
**Status**: Production Ready ✅
