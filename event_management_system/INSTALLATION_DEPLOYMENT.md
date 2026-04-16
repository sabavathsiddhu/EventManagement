# INSTALLATION & DEPLOYMENT GUIDE

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Docker Deployment](#docker-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Troubleshooting](#troubleshooting)
7. [Performance Optimization](#performance-optimization)

---

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows
- **Python**: 3.8 or higher
- **MySQL**: 5.7 or higher
- **RAM**: Minimum 2GB
- **Storage**: Minimum 5GB

### Software Requirements
```bash
# Windows
- Git for Windows
- Visual C++ Redistributable
- Python 3.8+

# Linux (Ubuntu)
sudo apt-get update
sudo apt-get install python3-dev python3-pip mysql-server git

# macOS
brew install python@3.9 mysql
```

---

## Local Development Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd event_management_system
```

### Step 2: Create Python Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database

**Create MySQL Database:**
```sql
CREATE DATABASE event_management_system;
USE event_management_system;
```

**Or Run Schema:**
```bash
mysql -u root -p event_management_system < database/schema.sql
```

### Step 5: Configure Environment
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your configuration
```

**Edit .env file:**
```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=event_management_system
SECRET_KEY=your_secret_key
DEBUG=True
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_secret_key
```

### Step 6: Run Application
```bash
python app.py
```

Access at: http://localhost:5000

---

## Production Deployment

### Step 1: Prepare Server

**AWS EC2 Ubuntu Setup:**
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3-pip python3-venv mysql-server nginx supervisor git

# Create application user
sudo useradd -m -s /bin/bash appuser
sudo su - appuser
```

### Step 2: Clone and Setup Application
```bash
cd /home/appuser
git clone <repository-url>
cd event_management_system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production server
pip install gunicorn
```

### Step 3: Configure MySQL
```bash
sudo mysql -u root -p

# In MySQL console:
CREATE DATABASE event_management_system CHARACTER SET utf8mb4;
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON event_management_system.* TO 'appuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# Import schema
mysql -u appuser -p event_management_system < database/schema.sql
```

### Step 4: Configure Environment
```bash
nano .env
```

**Production .env:**
```env
FLASK_ENV=production
DEBUG=False
MYSQL_HOST=localhost
MYSQL_USER=appuser
MYSQL_PASSWORD=secure_password
MYSQL_DB=event_management_system
SECRET_KEY=generate_random_secure_key_here
RAZORPAY_KEY_ID=your_production_key_id
RAZORPAY_KEY_SECRET=your_production_secret
SESSION_TIMEOUT=7200
```

### Step 5: Configure Gunicorn
```bash
# Create gunicorn config file
nano gunicorn_config.py
```

**gunicorn_config.py:**
```python
import multiprocessing

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
```

### Step 6: Configure Supervisor
```bash
sudo nano /etc/supervisor/conf.d/event_management.conf
```

**Configuration:**
```ini
[program:event_management]
directory=/home/appuser/event_management_system
command=/home/appuser/event_management_system/venv/bin/gunicorn \
    --config gunicorn_config.py app:app

user=appuser
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=10
stdout_logfile=/var/log/event_management/access.log
stderr_logfile=/var/log/event_management/error.log

[group:theweb]
programs=event_management
```

**Create log directory:**
```bash
sudo mkdir -p /var/log/event_management
sudo chown appuser:appuser /var/log/event_management
```

### Step 7: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/event_management
```

**Nginx Configuration:**
```nginx
upstream event_management {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your_domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your_domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your_domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your_domain.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/event_management_access.log;
    error_log /var/log/nginx/event_management_error.log;

    # Location
    location / {
        proxy_pass http://event_management;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files
    location /static/ {
        alias /home/appuser/event_management_system/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # File upload limit
    client_max_body_size 16M;
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/event_management /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### Step 8: Setup SSL with Let's Encrypt
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d your_domain.com
```

### Step 9: Start Services
```bash
# Reload supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start event_management

# Restart Nginx
sudo systemctl restart nginx

# Check status
sudo supervisorctl status
```

---

## Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: event_management_system
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppassword
    volumes:
      - mysql_data:/var/lib/mysql
      - ./database/schema.sql:/docker-entrypoint-initdb.d/schema.sql
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      MYSQL_HOST: mysql
      MYSQL_USER: appuser
      MYSQL_PASSWORD: apppassword
      MYSQL_DB: event_management_system
      SECRET_KEY: your_secret_key
    depends_on:
      mysql:
        condition: service_healthy
    volumes:
      - ./certificates:/app/certificates
      - ./face_recognition:/app/face_recognition

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web

volumes:
  mysql_data:
```

**Deploy with Docker Compose:**
```bash
docker-compose up -d
```

---

## Cloud Deployment

### AWS Elastic Beanstalk

**Create .ebextensions/python.config:**
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
```

**Deploy:**
```bash
eb init
eb create event-management-env
eb deploy
```

### Heroku Deployment

**Create Procfile:**
```
web: gunicorn app:app
```

**Create runtime.txt:**
```
python-3.9.0
```

**Deploy:**
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your_secret_key
```

---

## Troubleshooting

### Database Connection Issues
```bash
# Test MySQL connection
mysql -h localhost -u appuser -p -D event_management_system

# Check MySQL logs
sudo tail -f /var/log/mysql/error.log
```

### Face Recognition Issues
```bash
# Install dependencies
pip install --upgrade opencv-python
pip install --upgrade face-recognition

# Test webcam
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Certificate Generation Issues
```bash
# Create certificates directory
mkdir -p certificates
chmod 755 certificates

# Check permissions
ls -la certificates
```

### Application Logs
```bash
# Supervisor logs
sudo tail -f /var/log/event_management/error.log

# Nginx logs
sudo tail -f /var/log/nginx/event_management_error.log

# Application logs
tail -f app.log
```

---

## Performance Optimization

### Database Optimization
```sql
-- Add indexes
CREATE INDEX idx_student_email ON students(email);
CREATE INDEX idx_event_date ON events(event_date);
CREATE INDEX idx_registration_status ON registrations(registration_status);
CREATE INDEX idx_payment_status ON payments(payment_status);

-- Enable query cache (MySQL 5.7)
SET GLOBAL query_cache_type = 1;
SET GLOBAL query_cache_size = 268435456;
```

### Caching Strategy
```python
# Redis Configuration in app/config.py
import redis

CACHE_REDIS_URL = "redis://localhost:6379/0"
CACHE_TYPE = "redis"
```

### Load Balancing
```nginx
upstream app_servers {
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
    server 127.0.0.1:5004;
}
```

### CDN Configuration
```
CloudFront Distribution:
- Origin: Your domain
- Behaviors: /static/* → CloudFront
- TTL: 30 days for static files
```

---

## Security Checklist

- [ ] Change default admin password
- [ ] Update SECRET_KEY in production
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up database backups
- [ ] Enable audit logging
- [ ] Configure rate limiting
- [ ] Set up intrusion detection
- [ ] Regular security updates
- [ ] Database encryption at rest

---

## Backup & Recovery

### MySQL Backup
```bash
# Daily backup
mysqldump -u appuser -p event_management_system > backup_$(date +%Y%m%d).sql

# Restore
mysql -u appuser -p event_management_system < backup_*.sql
```

### Automated Backup (Cron)
```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * mysqldump -u appuser -p'password' event_management_system > /backups/db_$(date +\%Y\%m\%d).sql

# Keep only last 30 days
find /backups -name "db_*.sql" -mtime +30 -delete
```

---

## Monitoring & Maintenance

### Server Monitoring
```bash
# Install monitoring
sudo apt-get install htop iotop nethogs

# Monitor resources
htop
```

### Application Monitoring
```python
# Add to app.py
from flask_sqlalchemy import SQLAlchemy
from healthcheck import HealthCheck

health = HealthCheck()

def database_available():
    try:
        db.session.execute('SELECT 1')
        return True, "Database connection ok"
    except Exception as e:
        return False, f"Database connection failed: {e}"

health.add(database_available, "Database Available")
```

---

For more information, consult the main README.md file.
