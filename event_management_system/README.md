# Smart Campus Event Management System - README

## Overview

Smart Campus Event Management System is a comprehensive, production-ready Flask web application designed to manage campus events with advanced features including:

- **Three User Roles**: Students, Administrators, and Event Organisers
- **Face Recognition Attendance**: Automated attendance marking using OpenCV
- **Certificate Generation**: Automatic certificate creation using ReportLab
- **Payment Integration**: Razorpay integration for paid events
- **Eligibility Management**: CGPA and attendance-based event registration
- **Real-time Analytics**: Comprehensive dashboards and reports

## Project Structure

```
event_management_system/
├── app/
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── routes/
│   │   ├── auth_routes.py          # Authentication routes
│   │   ├── student_routes.py       # Student module routes
│   │   ├── admin_routes.py         # Admin module routes
│   │   └── organiser_routes.py     # Event organiser routes
│   ├── modules/
│   │   ├── face_recognition_module.py   # Face recognition
│   │   ├── certificate_module.py        # Certificate generation
│   │   └── payment_module.py            # Payment processing
│   ├── templates/
│   │   ├── base.html               # Base template
│   │   ├── index.html              # Home page
│   │   ├── auth/                   # Authentication templates
│   │   ├── student/                # Student templates
│   │   ├── admin/                  # Admin templates
│   │   ├── organiser/              # Organiser templates
│   │   └── errors/                 # Error pages
│   └── static/
│       ├── css/style.css           # Main stylesheet
│       ├── js/main.js              # JavaScript utilities
│       └── images/                 # Images
├── database/
│   └── schema.sql                  # Database schema
├── utils/
│   ├── auth.py                     # Authentication utilities
│   ├── database.py                 # Database connection
│   └── validation.py               # Input validation
├── certificates/                   # Generated certificates folder
├── face_recognition/               # Face encodings folder
├── app.py                          # Main application file
├── setup.py                        # Setup script
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
└── README.md                       # This file
```

## Features

### 1. Student Module
- User registration with profile information
- View available events with eligibility criteria
- Register for events (with eligibility validation)
- Make payments for paid events (Razorpay)
- View participation status
- Download certificates after event completion
- Manage profile (CGPA, attendance)

### 2. Admin Module
- Complete dashboard with statistics
- Create, edit, and delete events
- Define eligibility criteria (CGPA, attendance)
- Assign event organisers
- View all student registrations
- Monitor payments and revenue
- View analytics and reports
- Manage event organisers

### 3. Event Organiser Module
- View assigned events
- Mark student attendance (manual or face recognition)
- View registered students list
- Generate and issue certificates
- Track event participation

### 4. Advanced Features

#### Face Recognition Attendance
- Capture student faces during registration
- Use face recognition for attendance marking
- Automatic face encoding storage
- Real-time student identification

#### Certificate Generation
- Professional PDF certificate generation
- Unique certificate numbers
- Automatic generation after event completion
- Download tracking

#### Payment Integration
- Razorpay payment gateway integration
- Secure payment processing
- Payment status tracking
- Refund support

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Webcam (for face recognition)

### Step 1: Clone/Download the Project
```bash
cd event_management_system
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
python setup.py
```

This will guide you through:
- Checking all dependencies
- Configuring MySQL database
- Setting up Razorpay credentials
- Creating necessary directories

### Step 4: Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:5000`

## Database Setup

The system automatically creates all necessary tables. The database schema includes:

- **students**: Student user profiles
- **admin**: Administrator accounts
- **event_organisers**: Event organiser accounts
- **events**: Event information and criteria
- **registrations**: Student event registrations
- **payments**: Payment records
- **attendance**: Attendance tracking
- **certificates**: Issued certificates

## Default Credentials

### Admin Login
- **Email**: admin@campus.edu
- **Password**: admin123
- **Note**: Change this password in production!

### To Register
1. Visit: `http://localhost:5000/auth/register/student`
2. Fill in your details
3. Login with your credentials

## Configuration

### Environment Variables (.env)

```env
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=event_management_system

# Flask Configuration
SECRET_KEY=your-secret-key
DEBUG=True

# Razorpay Configuration
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret

# Session Configuration
SESSION_TIMEOUT=3600
```

### Razorpay Setup

1. Create account at https://razorpay.com
2. Get your API keys from dashboard
3. Update credentials in .env file
4. Test mode credentials can be used for development

## Usage Examples

### Student Workflow
1. Register as a student
2. View available events matching your criteria
3. Register for events
4. Attend events (marked by organiser)
5. Download certificates

### Admin Workflow
1. Login as admin
2. Create events with eligibility criteria
3. Assign organisers to events
4. Monitor registrations and payments
5. View analytics

### Organiser Workflow
1. Login as organiser
2. View assigned events
3. Mark attendance (automatic or manual)
4. Generate certificates for attendees
5. Track event participation

## Security Features

- **Bcrypt Password Hashing**: Secure password storage
- **Session Management**: Automatic session timeout
- **CSRF Protection**: Built-in form validation
- **SQL Injection Prevention**: Parameterized queries
- **XSS Prevention**: Input sanitization
- **Role-Based Access Control**: Proper authorization

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register/student` - Student registration
- `POST /auth/register/organiser` - Organiser registration
- `GET /logout` - User logout

### Student
- `GET /student/dashboard` - Student dashboard
- `GET /student/events` - View available events
- `POST /student/register/<event_id>` - Register for event
- `GET /student/certificates` - View certificates
- `GET /student/download/<certificate_id>` - Download certificate
- `GET /student/profile` - View profile
- `POST /student/profile/update` - Update profile

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/events` - Manage events
- `POST /admin/event/create` - Create event
- `POST /admin/event/<id>/edit` - Edit event
- `POST /admin/event/<id>/delete` - Delete event
- `GET /admin/registrations` - View registrations
- `GET /admin/students` - Manage students
- `GET /admin/analytics` - View analytics

### Organiser
- `GET /organiser/dashboard` - Organiser dashboard
- `GET /organiser/event/<id>` - View event details
- `GET /organiser/attendance/<id>` - Mark attendance
- `POST /organiser/attendance/save` - Save attendance
- `GET /organiser/certificates/<id>` - Generate certificates
- `POST /organiser/certificates/generate` - Create certificates

## Troubleshooting

### Issue: Database connection failed
**Solution**: 
- Check MySQL is running
- Verify credentials in .env
- Ensure database exists

### Issue: Face recognition not working
**Solution**:
- Ensure webcam is connected
- Check OpenCV installation: `pip install opencv-python`
- Verify face-recognition package: `pip install face-recognition`

### Issue: Certificates not generating
**Solution**:
- Check ReportLab installation: `pip install reportlab`
- Verify `certificates/` directory exists
- Check file permissions

### Issue: Razorpay payment fails
**Solution**:
- Verify API credentials in .env
- Check test mode is enabled
- Verify payment amount is in paise

## Performance Tips

1. **Database Indexing**: Indexes are already created
2. **Caching**: Implement Redis for session caching
3. **Load Balancing**: Use Gunicorn with multiple workers
4. **CDN**: Serve static files from CDN
5. **Database Optimization**: Regular maintenance and backups

## Future Enhancements

1. **Mobile Application**: React Native app for mobile access
2. **AI Analytics**: Predictive analytics for event attendance
3. **Email Notifications**: Automated email alerts
4. **QR Code Generation**: QR codes for event entry
5. **SMS Integration**: SMS notifications
6. **Video Conferencing**: Virtual event support
7. **Advanced Reporting**: PDF report generation
8. **Blockchain Certificates**: Verifiable certificates
9. **API Rate Limiting**: Better API protection
10. **Microservices**: Scalable architecture

## Deployment

### Using Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### On Heroku
```bash
heroku create your-app-name
git push heroku main
```

## Support & Documentation

- **Official Docs**: See inline code comments
- **Database**: See database/schema.sql
- **API**: See docstrings in route handlers
- **Configuration**: See app/config.py

## License

This project is provided as-is for educational purposes.

## Contributors

- Development Team
- Campus IT Department

## Contact

For support and queries:
- Email: support@campus.edu
- Website: https://campus.edu
- Phone: +91-9999-9999

---

**Version**: 1.0.0  
**Last Updated**: April 2024  
**Status**: Production Ready
