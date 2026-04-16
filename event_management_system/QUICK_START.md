# Quick Start Guide - Smart Campus Event Management System

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Database
```bash
# Update .env file with your MySQL credentials
# MySQL Host: localhost
# MySQL User: root
# MySQL Password: root (or your password)
# Database: event_management_system
```

### 3. Setup Database
```bash
# Run this in MySQL
mysql -u root -p < database/schema.sql
```

### 4. Run Application
```bash
python app.py
```

### 5. Access Application
- URL: http://localhost:5000
- Admin Email: admin@campus.edu
- Admin Password: admin123
- App starts on port 5000

---

## 📁 Project Structure

```
event_management_system/
├── app/                              # Main Flask application
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── routes/
│   │   ├── auth_routes.py          # Login/Register
│   │   ├── student_routes.py       # Student features
│   │   ├── admin_routes.py         # Admin dashboard
│   │   └── organiser_routes.py     # Organiser features
│   ├── modules/
│   │   ├── face_recognition_module.py   # Face recognition
│   │   ├── certificate_module.py        # Certificate generation
│   │   └── payment_module.py            # Payment processing (Razorpay)
│   ├── templates/
│   │   ├── base.html               # Base template
│   │   ├── index.html              # Home page
│   │   ├── auth/                   # Authentication templates
│   │   │   ├── login.html
│   │   │   ├── register_student.html
│   │   │   └── register_organiser.html
│   │   ├── student/                # Student module
│   │   │   ├── dashboard.html
│   │   │   ├── events.html
│   │   │   ├── payment.html
│   │   │   ├── certificates.html
│   │   │   └── profile.html
│   │   ├── admin/                  # Admin module
│   │   │   ├── dashboard.html
│   │   │   ├── events.html
│   │   │   ├── create_event.html
│   │   │   ├── edit_event.html
│   │   │   ├── students.html
│   │   │   ├── registrations.html
│   │   │   ├── analytics.html
│   │   │   └── organisers.html
│   │   ├── organiser/              # Organiser module
│   │   │   ├── dashboard.html
│   │   │   ├── event_details.html
│   │   │   ├── mark_attendance.html
│   │   │   ├── generate_certificates.html
│   │   │   └── profile.html
│   │   └── errors/                 # Error pages
│   │       ├── 404.html
│   │       ├── 500.html
│   │       └── 403.html
│   └── static/
│       ├── css/style.css           # Stylesheet
│       ├── js/main.js              # JavaScript utilities
│       └── images/                 # Images
│
├── database/
│   └── schema.sql                  # Database schema
│
├── utils/
│   ├── auth.py                     # Authentication utilities
│   ├── database.py                 # Database connection
│   └── validation.py               # Input validation
│
├── certificates/                   # Generated certificates folder
├── face_recognition/               # Face recognition data
├── app.py                          # Main application
├── setup.py                        # Setup script
├── requirements.txt                # Python dependencies
├── .env                            # Configuration file
├── README.md                       # Full documentation
├── INSTALLATION_DEPLOYMENT.md      # Deployment guide
└── QUICK_START.md                  # This file
```

---

## 🛠️ Features Overview

### Student Module
```
Dashboard → View Events → Register → Payment → Get Certificate
```
- Browse available events
- Register for events (check eligibility)
- Make payments
- Download certificates

### Admin Module
```
Dashboard → Manage Events → Monitor Registrations → View Analytics
```
- Create and manage events
- Set eligibility criteria
- Assign organisers
- Track payments and analytics

### Event Organiser Module
```
Dashboard → Mark Attendance → Generate Certificates
```
- View assigned events
- Mark attendance (manual/face recognition)
- Generate and issue certificates

---

## 📊 Database Schema

### Key Tables
1. **students** - Student user accounts
2. **admin** - Administrator accounts
3. **event_organisers** - Event organiser accounts
4. **events** - Event information
5. **registrations** - Event registrations
6. **payments** - Payment records
7. **attendance** - Attendance tracking
8. **certificates** - Certificate records

---

## 🔑 Default Credentials

| User Type | Email | Password |
|-----------|-------|----------|
| Admin | admin@campus.edu | admin123 |

**⚠️ Important: Change these credentials in production!**

---

## 🌐 API Endpoints

### Authentication
- `POST /auth/login` - Login
- `POST /auth/register/student` - Student registration
- `GET /logout` - Logout

### Student
- `GET /student/dashboard` - Dashboard
- `GET /student/events` - View events
- `POST /student/register/<id>` - Register for event
- `GET /student/certificates` - View certificates

### Admin
- `GET /admin/dashboard` - Dashboard
- `GET /admin/events` - Manage events
- `POST /admin/event/create` - Create event
- `GET /admin/registrations` - View registrations

### Organiser
- `GET /organiser/dashboard` - Dashboard
- `GET /organiser/attendance/<id>` - Mark attendance
- `POST /organiser/certificates/generate` - Generate certificates

---

## ⚙️ Configuration (.env)

```env
# MySQL Configuration
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=event_management_system

# Flask Configuration
SECRET_KEY=your_secret_key_here
DEBUG=True

# Razorpay Configuration
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_secret

# Session Configuration
SESSION_TIMEOUT=3600
```

---

## 🐛 Troubleshooting

### Issue: Database Connection Failed
```bash
# Solution:
1. Verify MySQL is running
2. Check credentials in .env
3. Ensure database exists: mysql -u root -p < database/schema.sql
```

### Issue: Flask App Won't Start
```bash
# Solution:
1. Activate virtual environment
2. Install dependencies: pip install -r requirements.txt
3. Check Python version: python --version (should be 3.8+)
```

### Issue: Face Recognition Not Working
```bash
# Solution:
1. Install OpenCV: pip install opencv-python
2. Check webcam: python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

---

## 📚 Documentation

- **Full Documentation**: See `README.md`
- **Deployment Guide**: See `INSTALLATION_DEPLOYMENT.md`
- **Database Schema**: See `database/schema.sql`
- **API Details**: Check docstrings in route files

---

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker
```bash
docker build -t event_management .
docker run -p 5000:5000 event_management
```

---

## 🔐 Security Tips

1. **Change default password** before production
2. **Generate strong SECRET_KEY**:
   ```python
   import secrets
   secrets.token_hex(32)
   ```
3. **Enable HTTPS** in production
4. **Update dependencies** regularly
5. **Use environment variables** for secrets
6. **Enable database backups**

---

## 📈 Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python, Flask |
| Database | MySQL |
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Face Recognition | OpenCV, face_recognition |
| Certificates | ReportLab |
| Payments | Razorpay |
| Server | Nginx, Gunicorn |

---

## 📝 Development Workflow

### Adding New Feature
1. Create route in appropriate `_routes.py`
2. Create template in `templates/`
3. Add database queries in route handler
4. Test locally
5. Update documentation

### Example: New Student Feature
```python
# In app/routes/student_routes.py
@student_bp.route('/new-feature')
@login_required('student')
def new_feature():
    # Your code here
    return render_template('student/new_feature.html')
```

---

## 🤝 Contributing

1. Follow the existing code structure
2. Use meaningful variable names
3. Add comments for complex logic
4. Test before committing
5. Update documentation

---

## 📞 Support

- **Email**: support@campus.edu
- **Documentation**: README.md
- **Issues**: Check troubleshooting section

---

## 📜 License

This project is provided for educational purposes.

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Configure database
3. ✅ Run application
4. ✅ Login as admin
5. ✅ Create events
6. ✅ Register students
7. ✅ Test payment integration
8. ✅ Generate certificates

---

**Version**: 1.0.0  
**Last Updated**: April 2024  
**Status**: Production Ready ✅
