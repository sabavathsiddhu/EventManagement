# Setup script for Smart Campus Event Management System

import json
import sys
import os

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ {text}")

def check_requirements():
    """Check if all requirements are available"""
    print_header("Checking Requirements")
    
    try:
        import pymysql
        print_success("pymysql is installed")
    except ImportError:
        print_error("pymysql is not installed. Install with: pip install pymysql")
        return False
    
    try:
        import flask
        print_success("Flask is installed")
    except ImportError:
        print_error("Flask is not installed. Install with: pip install flask")
        return False
    
    try:
        import cv2
        print_success("OpenCV is installed")
    except ImportError:
        print_error("OpenCV is not installed. Install with: pip install opencv-python")
        return False
    
    try:
        import face_recognition
        print_success("Face Recognition is installed")
    except ImportError:
        print_error("Face Recognition is not installed. Install with: pip install face-recognition")
        return False
    
    try:
        import reportlab
        print_success("ReportLab is installed")
    except ImportError:
        print_error("ReportLab is not installed. Install with: pip install reportlab")
        return False
    
    try:
        import razorpay
        print_success("Razorpay is installed")
    except ImportError:
        print_error("Razorpay is not installed. Install with: pip install razorpay")
        return False
    
    return True

def generate_secret_key():
    """Generate a secure secret key"""
    import secrets
    return secrets.token_hex(32)

def update_env_file():
    """Update .env file with configuration"""
    print_header("Configuring Environment")
    
    env_file = '.env'
    
    config = {}
    config['SECRET_KEY'] = generate_secret_key()
    
    print_info("Enter MySQL Configuration:")
    config['MYSQL_HOST'] = input("MySQL Host (default: localhost): ") or "localhost"
    config['MYSQL_USER'] = input("MySQL User (default: root): ") or "root"
    config['MYSQL_PASSWORD'] = input("MySQL Password: ") or "root"
    config['MYSQL_DB'] = input("Database Name (default: event_management_system): ") or "event_management_system"
    
    print_info("\nEnter Razorpay Configuration (optional):")
    config['RAZORPAY_KEY_ID'] = input("Razorpay Key ID: ") or "your_razorpay_key_id"
    config['RAZORPAY_KEY_SECRET'] = input("Razorpay Key Secret: ") or "your_razorpay_key_secret"
    
    config['DEBUG'] = 'True'
    config['SESSION_TIMEOUT'] = '3600'
    
    # Write to .env file
    with open(env_file, 'w') as f:
        for key, value in config.items():
            f.write(f"{key}={value}\n")
    
    print_success(f"Configuration saved to {env_file}")

def setup_database():
    """Setup database"""
    print_header("Setting Up Database")
    
    try:
        import pymysql
        from app.config import Config
        
        # Read MySQL config from .env
        from dotenv import load_dotenv
        load_dotenv()
        
        host = os.getenv('MYSQL_HOST', 'localhost')
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', 'root')
        database = os.getenv('MYSQL_DB', 'event_management_system')
        
        # Connect to MySQL without database
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # Read and execute schema
        with open('database/schema.sql', 'r') as f:
            schema = f.read()
            
            # Split by semicolon and execute
            statements = schema.split(';')
            for statement in statements:
                if statement.strip():
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        # Some errors are expected (like duplicate key)
                        pass
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print_success("Database setup completed")
        
    except Exception as e:
        print_error(f"Database setup failed: {e}")
        print_info("Please check your MySQL installation and credentials")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = [
        'app/templates/student',
        'app/templates/admin',
        'app/templates/organiser',
        'app/templates/auth',
        'app/templates/errors',
        'app/static/uploads',
        'certificates',
        'face_recognition',
        'logs'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print_success(f"Created directory: {directory}")
        else:
            print_info(f"Directory already exists: {directory}")

def print_next_steps():
    """Print next steps"""
    print_header("Setup Complete!")
    
    print("Next Steps:")
    print("-" * 60)
    print("\n1. Verify your MySQL database is running")
    print("2. Check your .env file for configuration")
    print("3. Update Razorpay credentials if needed")
    print("4. Run the application:")
    print("\n   python app.py")
    print("\n5. Access the application at: http://localhost:5000")
    print("\n6. Default Admin Credentials:")
    print("   Email: admin@campus.edu")
    print("   Password: admin123 (CHANGE THIS IN PRODUCTION)")
    print("\n7. Student Registration: http://localhost:5000/auth/register/student")
    print("\n" + "="*60 + "\n")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  Smart Campus Event Management System - Setup")
    print("="*60 + "\n")
    
    # Check requirements
    if not check_requirements():
        print_error("Some requirements are missing. Please install them first.")
        print_info("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Update configuration
    update_env_file()
    
    # Setup database
    if not setup_database():
        print_error("Database setup failed. Please check your configuration.")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == '__main__':
    main()
