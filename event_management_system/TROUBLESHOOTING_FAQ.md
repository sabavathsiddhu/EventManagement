# 🔧 Troubleshooting & FAQ - Smart Campus Event Management System

**Quick solutions to common problems and frequently asked questions.**

---

## ❓ Frequently Asked Questions (FAQ)

### Getting Started

#### Q1: How do I start the application?
**A:** Run this command:
```bash
python app.py
```
App will start at `http://localhost:5000`

---

#### Q2: What are the default credentials?
**A:** 
```
Email: admin@campus.edu
Password: admin123
Role: Admin
```
⚠️ **Important**: Change these in production!

---

#### Q3: Do I need to install MySQL separately?
**A:** Yes. Instructions in [INSTALLATION_DEPLOYMENT.md](INSTALLATION_DEPLOYMENT.md#prerequisites)

---

#### Q4: What Python version do I need?
**A:** Python **3.8 or higher**

Check your version:
```bash
python --version
```

---

#### Q5: How do I create a virtual environment?
**A:**
```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

---

### User Roles & Access

#### Q6: What are the three user roles?
**A:**
1. **Student** - Register for events, pay, get certificates
2. **Admin** - Manage all events and users
3. **Organiser** - Mark attendance, generate certificates

---

#### Q7: Can a student be an admin?
**A:** No, roles are separate. Each role has its own login.

---

#### Q8: How do I reset a user password?
**A:** Currently, admin must manually reset in database:
```sql
UPDATE students SET password_hash = 'new_bcrypt_hash' WHERE student_id = 1;
```

---

#### Q9: What is session timeout?
**A:** Users are automatically logged out after **3600 seconds (1 hour)** of inactivity.

---

### Events & Registration

#### Q10: How does event eligibility work?
**A:** Student must meet BOTH criteria:
- CGPA ≥ event's minimum CGPA
- Attendance % ≥ event's minimum attendance

---

#### Q11: Can students register for free events?
**A:** Yes, they can register directly without payment.

---

#### Q12: What happens if a student doesn't meet eligibility?
**A:** They see an error with reasons:
```
❌ Not eligible for this event
- Your CGPA (7.5) is below minimum (8.0)
- Your attendance (75%) is below minimum (80%)
```

---

#### Q13: Can students change their CGPA?
**A:** Students can update their own CGPA in profile, but admin can also override it.

---

#### Q14: What is the maximum event fee?
**A:** No limit (can be set by admin when creating event).

---

### Payments

#### Q15: Which payment gateway is used?
**A:** **Razorpay** - popular in India. Accepts credit/debit cards, UPI, etc.

---

#### Q16: Do I need live Razorpay credentials?
**A:** For testing: Use Razorpay **test credentials** from your dashboard.

---

#### Q17: Can students get refunds?
**A:** Yes, admin can process refunds through Razorpay.

---

#### Q18: What payment statuses exist?
**A:**
- **pending** - Payment not yet verified
- **completed** - Payment successful
- **failed** - Payment failed
- **refunded** - Refund processed

---

#### Q19: Are payments encrypted?
**A:** Yes, HMAC-SHA256 signature verification ensures secure transactions.

---

### Attendance & Certificates

#### Q20: What are two ways to mark attendance?
**A:**
1. **Manual** - Organiser manually checks off students
2. **Face Recognition** - Real-time camera-based detection

---

#### Q21: Can attendance be marked before event date?
**A:** Yes, it can be marked any time by organiser.

---

#### Q22: How long does certificate generation take?
**A:** Usually **< 5 seconds** for 50 students (batch processing).

---

#### Q23: Can certificates be regenerated?
**A:** Yes, organiser can generate again (creates new certificate with different number).

---

#### Q24: What format are certificates in?
**A:** **PDF** (11" × 8.5" landscape with professional design).

---

#### Q25: Can certificates be downloaded?
**A:** Yes, students can download from dashboard. Download count is tracked.

---

### Face Recognition

#### Q26: What are hardware requirements for face recognition?
**A:**
- Webcam (built-in or USB)
- Adequate lighting
- Python packages installed

---

#### Q27: Why doesn't face recognition work?
**A:** Common causes:
1. Webcam not connected or not working
2. OpenCV not installed
3. Poor lighting conditions
4. Face not clearly visible to camera

**Solution**: See [Face Recognition Troubleshooting](#face-recognition-issues)

---

#### Q28: Can face recognition be used offline?
**A:** Yes, all processing is local (no cloud dependency).

---

#### Q29: How is face data stored?
**A:** Face encodings (mathematical vectors, not images) are stored as pickle files.

---

#### Q30: Is face data deleted after event?
**A:** Yes, can be deleted by admin after event completion.

---

---

## 🐛 Troubleshooting Guide

### Database Issues

#### Problem: "Can't connect to MySQL server"
**Error Message:**
```
MySQLError: Can't connect to MySQL server
Connection refused (111)
```

**Solutions:**
1. **Check MySQL is running:**
   ```bash
   # Windows
   services.msc  # Look for MySQL service
   
   # Mac
   brew services list | grep mysql
   
   # Linux
   sudo systemctl status mysql
   ```

2. **Verify credentials in `.env`:**
   ```env
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DB=event_management_system
   ```

3. **Check database exists:**
   ```sql
   mysql -u root -p
   SHOW DATABASES;
   ```

4. **Recreate database:**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

---

#### Problem: "Table doesn't exist"
**Error Message:**
```
ProgrammingError: Table 'event_management_system.students' doesn't exist
```

**Solution:** Run schema:
```bash
mysql -u root -p event_management_system < database/schema.sql
```

---

#### Problem: "Access denied for user 'root'@'localhost'"
**Error Message:**
```
MySQLError: Access denied for user 'root'@'localhost' (using password: YES)
```

**Solutions:**
1. Verify password in `.env` is correct
2. Reset MySQL root password:
   ```bash
   # Windows
   mysqld --skip-grant-tables
   mysql -u root
   FLUSH PRIVILEGES;
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
   ```

3. Check MySQL user permissions:
   ```sql
   mysql -u root -p
   SHOW GRANTS FOR 'root'@'localhost';
   ```

---

### Flask Application Issues

#### Problem: "Port 5000 is already in use"
**Error Message:**
```
OSError: [Errno 48] Address already in use
```

**Solutions:**
1. **Kill process using port 5000:**
   ```bash
   # Windows (PowerShell)
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # Mac/Linux
   lsof -i :5000
   kill -9 <PID>
   ```

2. **Use different port:**
   ```python
   # In app.py
   if __name__ == '__main__':
       app.run(port=5001)  # Changed from 5000
   ```

---

#### Problem: "ModuleNotFoundError: No module named 'flask'"
**Error Message:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:** Install dependencies:
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

---

#### Problem: "App won't start - syntax error"
**Error Message:**
```
SyntaxError: invalid syntax
```

**Solution:**
1. Check Python version (must be 3.8+)
2. Look at error line number
3. Fix syntax and restart

---

#### Problem: "Secret key not set"
**Error Message:**
```
RuntimeError: The session interface is not properly configured
```

**Solution:** Ensure `.env` has:
```env
SECRET_KEY=your-super-secret-key-here-change-in-production
```

---

### Face Recognition Issues

#### Problem 1: "ImportError: No module named 'cv2'"
**Error Message:**
```
ImportError: No module named 'cv2'
```

**Solution:** Install OpenCV:
```bash
pip install opencv-python
pip install face-recognition
```

---

#### Problem 2: "Webcam not detected"
**Symptoms:** Camera window doesn't open, no video feed

**Solutions:**
1. **Check if webcam is connected:**
   ```python
   import cv2
   cap = cv2.VideoCapture(0)
   print(cap.isOpened())  # Should print True
   ```

2. **Try different camera index:**
   ```python
   # Try camera indices 0, 1, 2...
   cap = cv2.VideoCapture(1)  # Try 1 instead of 0
   ```

3. **Check permissions (Mac/Linux):**
   ```bash
   # Mac - grant camera permission in System Preferences
   # Linux - add user to video group
   sudo usermod -a -G video $USER
   ```

---

#### Problem 3: "Face not being recognized"
**Symptoms:** Camera opens but faces aren't detected

**Solutions:**
1. **Improve lighting** - Face recognition works better in good lighting
2. **Get closer to camera** - Move face 0.5-1 meter from camera
3. **Check face is fully visible** - Both eyes, nose, mouth visible
4. **Lower recognition threshold** (in `face_recognition_module.py`):
   ```python
   tolerance=0.6  # Increase to 0.7 for more lenient matching
   ```

---

#### Problem 4: "Face recognition is slow"
**Symptoms:** Takes > 1 second per face

**Solution options:**
1. Reduce image resolution
2. Use GPU acceleration if available
3. Batch process faces

---

### Payment Issues

#### Problem 1: "Razorpay credentials invalid"
**Error Message:**
```
Unauthorized: Invalid Razorpay credentials
```

**Solution:**
1. Get credentials from [Razorpay Dashboard](https://dashboard.razorpay.com)
2. Update `.env`:
   ```env
   RAZORPAY_KEY_ID=your_key_id
   RAZORPAY_KEY_SECRET=your_key_secret
   ```
3. Restart app

---

#### Problem 2: "Payment signature verification failed"
**Error Message:**
```
PaymentVerificationError: Signature verification failed
```

**Solutions:**
1. Verify Razorpay credentials in `.env`
2. Check payment amounts match (in paise = rupees × 100)
3. Look at order ID and payment ID match

---

#### Problem 3: "Payment gateway not responding"
**Solutions:**
1. Check internet connection
2. Verify API credentials
3. Check Razorpay service status
4. Try test credentials instead

---

### Authentication Issues

#### Problem 1: "Login fails for valid credentials"
**Solutions:**
1. **Check database has user:**
   ```sql
   SELECT * FROM students WHERE email = 'test@example.com';
   ```

2. **Reset password manually:**
   ```python
   from utils.auth import hash_password
   
   new_hash = hash_password('newpassword123')
   # Update in database
   ```

---

#### Problem 2: "Session expires too quickly"
**Solution:** Adjust timeout in `config.py`:
```python
SESSION_TIMEOUT = 7200  # 2 hours instead of 1
```

---

#### Problem 3: "Password validation too strict"
**Error:** "Password must contain..."

**Solution:** Review password requirements in `utils/auth.py`:
```python
def validate_password_strength(password):
    # Modify rules here
```

---

### Template & UI Issues

#### Problem 1: "Template not found"
**Error Message:**
```
TemplateNotFound: dashboard.html
```

**Solution:**
1. Check file exists at `app/templates/student/dashboard.html`
2. Verify template name matches route
3. Check folder structure

---

#### Problem 2: "CSS/styling not loading"
**Solutions:**
1. Clear browser cache (Ctrl+Shift+Delete)
2. Check static folder path: `app/static/css/`
3. Verify Bootstrap CDN is accessible

---

#### Problem 3: "JavaScript errors"
**Solutions:**
1. Open browser console (F12)
2. Check error messages
3. Verify jQuery/Bootstrap loaded

---

### Certificate Generation Issues

#### Problem 1: "Certificate generation fails"
**Error Message:**
```
ReportLabError: Certificate generation failed
```

**Solutions:**
1. Ensure ReportLab installed:
   ```bash
   pip install reportlab
   ```

2. Check `certificates/` folder exists and is writable
3. Verify student data completeness

---

#### Problem 2: "PDF looks wrong"
**Solutions:**
1. Check font availability
2. Verify template in `certificate_module.py`
3. Test with different student name lengths

---

### Performance Issues

#### Problem: "App is slow"
**Solutions:**
1. **Add database indexes:** ✅ Already done in schema
2. **Check database queries:** Use slow query log
3. **Reduce images:** Compress images in `app/static/images/`
4. **Enable caching:** Use Flask caching

---

### Deployment Issues

#### Problem: "504 Bad Gateway on production"
**Solutions:**
1. Check Gunicorn is running
2. Verify Nginx configuration
3. Check application logs
4. Ensure database accessible

---

---

## 🖥️ System Requirements Verification

### Check All Requirements:
```bash
# Python version
python --version              # Should be 3.8+

# MySQL
mysql --version              # Should be 5.7+

# Installed packages
pip list | grep -E "flask|mysql|opencv"

# Webcam (for face recognition)
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"

# Disk space
df -h                        # Check available space
```

---

## 📊 Log Files

### Where to find logs:
```
logs/
├── app.log          # Application events
├── error.log        # Error messages
├── database.log     # Database queries
└── payment.log      # Payment transactions
```

### View logs:
```bash
# Recent errors
tail -f logs/error.log

# Search for specific error
grep "error_keyword" logs/error.log
```

---

## 🆘 Still Need Help?

### Check Documentation
1. [README.md](README.md) - Full documentation
2. [QUICK_START.md](QUICK_START.md) - Quick reference
3. [INSTALLATION_DEPLOYMENT.md](INSTALLATION_DEPLOYMENT.md) - Setup guide

### Debug Mode

Enable debug in `config.py`:
```python
DEBUG = True     # Shows detailed error pages
```

### Generate Diagnostic Report

```python
# In Python shell
import sys
print(f"Python: {sys.version}")
print(f"Platform: {sys.platform}")

import mysql
print(f"MySQLdb: {mysql.__version__}")

import cv2
print(f"OpenCV: {cv2.__version__}")
```

---

## 🔍 Common Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| **400** | Bad Request | Check form data |
| **401** | Unauthorized | Login required |
| **403** | Forbidden | No permission |
| **404** | Not Found | Check URL/resource |
| **500** | Server Error | Check logs |
| **DB001** | DB Connection Failed | Restart MySQL |
| **AUTH001** | Invalid Credentials | Check password |
| **PAY001** | Payment Failed | Check Razorpay |
| **FACE001** | Face Not Found | Add face encoding |

---

## ✅ Pre-Deployment Checklist

Before going to production:
- [ ] Update default credentials
- [ ] Set `DEBUG = False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Update `.env` with production credentials
- [ ] Set up SSL/TLS certificate
- [ ] Configure Nginx reverse proxy
- [ ] Enable database backups
- [ ] Test all features
- [ ] Monitor application

---

## 📈 Performance Tuning

### Database Optimization
```sql
-- Check query performance
EXPLAIN SELECT * FROM events WHERE event_date > NOW();

-- Add missing indexes
CREATE INDEX idx_event_date ON events(event_date);
```

### Application Optimization
```python
# In config.py
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300
```

---

## 🔐 Security Checklist

- [ ] Change default admin password
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall
- [ ] Regular backups
- [ ] Update dependencies
- [ ] Monitor logs
- [ ] Strong database password
- [ ] Limit file uploads
- [ ] Rate limiting

---

**Troubleshooting Guide Version**: 1.0.0  
**Last Updated**: April 2024  
**Status**: Complete ✅
