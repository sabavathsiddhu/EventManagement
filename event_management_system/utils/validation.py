"""
Validation Module
"""
from datetime import datetime
import re


class ValidationError(Exception):
    """Custom validation error"""
    pass


def validate_student_registration(data):
    """Validate student registration data"""
    errors = []
    
    # Name validation
    if not data.get('name') or len(data.get('name', '')) < 2:
        errors.append('Name must be at least 2 characters long')
    
    # Email validation
    email = data.get('email', '')
    if not email:
        errors.append('Email is required')
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors.append('Invalid email format')
    
    # Password validation
    password = data.get('password', '')
    if len(password) < 8:
        errors.append('Password must be at least 8 characters long')
    
    # CGPA validation
    try:
        cgpa = float(data.get('cgpa', 0))
        if not (0 <= cgpa <= 10):
            errors.append('CGPA must be between 0 and 10')
    except (ValueError, TypeError):
        errors.append('Invalid CGPA value')
    
    # Attendance validation
    try:
        attendance = float(data.get('attendance', 0))
        if not (0 <= attendance <= 100):
            errors.append('Attendance must be between 0 and 100')
    except (ValueError, TypeError):
        errors.append('Invalid attendance value')
    
    return errors


def validate_event_creation(data):
    """Validate event creation data"""
    errors = []
    
    # Event name validation
    if not data.get('event_name') or len(data.get('event_name', '')) < 3:
        errors.append('Event name must be at least 3 characters long')
    
    # Event date validation
    try:
        event_date = datetime.strptime(data.get('event_date', ''), '%Y-%m-%d')
        if event_date < datetime.now():
            errors.append('Event date must be in the future')
    except (ValueError, TypeError):
        errors.append('Invalid event date format (use YYYY-MM-DD)')
    
    # CGPA requirement validation
    try:
        min_cgpa = float(data.get('min_cgpa', 0))
        if not (0 <= min_cgpa <= 10):
            errors.append('Minimum CGPA must be between 0 and 10')
    except (ValueError, TypeError):
        errors.append('Invalid CGPA requirement')
    
    # Attendance requirement validation
    try:
        min_attendance = float(data.get('min_attendance', 0))
        if not (0 <= min_attendance <= 100):
            errors.append('Minimum attendance must be between 0 and 100')
    except (ValueError, TypeError):
        errors.append('Invalid attendance requirement')
    
    # Maximum capacity validation
    if data.get('is_paid') == 'on' or data.get('is_paid') == True:
        try:
            fee = float(data.get('event_fee', 0))
            if fee < 0:
                errors.append('Event fee cannot be negative')
        except (ValueError, TypeError):
            errors.append('Invalid event fee')
    
    return errors


def check_student_eligibility(student_cgpa, student_attendance, min_cgpa, min_attendance):
    """Check if student meets event eligibility criteria"""
    reasons = []
    
    if student_cgpa < min_cgpa:
        reasons.append(f'Minimum CGPA requirement: {min_cgpa} (Your CGPA: {student_cgpa})')
    
    if student_attendance < min_attendance:
        reasons.append(f'Minimum attendance requirement: {min_attendance}% (Your attendance: {student_attendance}%)')
    
    return len(reasons) == 0, reasons
