"""
Authentication and Security Module
"""
import bcrypt
import hashlib
import secrets
import re
from functools import wraps
from flask import session, redirect, url_for, flash, request, jsonify


def hash_password(password):
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password, hash_digest):
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hash_digest.encode('utf-8'))
    except (ValueError, TypeError):
        return False


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password):
    """
    Validate password strength
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"


def generate_secure_token(length=32):
    """Generate a secure random token"""
    return secrets.token_hex(length // 2)


def login_required(user_type='student'):
    """Decorator to check if user is logged in"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            session_key = f'{user_type}_id'
            
            # Check if user is logged in
            if session_key not in session:
                if request.is_json:
                    return jsonify({'error': 'Unauthorized'}), 401
                flash(f'Please log in first', 'warning')
                return redirect(url_for('auth.login'))
            
            # Check session timeout
            from flask import current_app
            import time
            
            last_activity = session.get('last_activity', 0)
            current_time = time.time()
            session_timeout = current_app.config['SESSION_TIMEOUT']
            
            if current_time - last_activity > session_timeout:
                session.clear()
                if request.is_json:
                    return jsonify({'error': 'Session expired'}), 401
                flash('Session expired. Please log in again', 'warning')
                return redirect(url_for('auth.login'))
            
            # Update last activity time
            session['last_activity'] = current_time
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def role_required(allowed_roles):
    """Decorator to check user role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get('role')
            
            if user_role not in allowed_roles:
                if request.is_json:
                    return jsonify({'error': 'Forbidden'}), 403
                flash('You do not have permission to access this page', 'danger')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def sanitize_input(user_input):
    """Sanitize user input to prevent XSS"""
    dangerous_chars = ['<', '>', '"', "'", '&', ';']
    for char in dangerous_chars:
        user_input = user_input.replace(char, '')
    return user_input.strip()


def log_activity(user_id, user_type, action, details=''):
    """Log user activity (optional feature)"""
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {user_type.upper()} {user_id}: {action} - {details}"
    # You can save this to a file or database
    print(log_entry)
