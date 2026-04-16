-- Smart Campus Event Management System Database Schema
-- Create Database
CREATE DATABASE IF NOT EXISTS event_management_system;
USE event_management_system;

-- =============================================
-- STUDENTS TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    cgpa DECIMAL(3, 2) DEFAULT 0.00,
    attendance DECIMAL(5, 2) DEFAULT 0.00 COMMENT 'Attendance percentage',
    phone VARCHAR(15),
    enrollment_number VARCHAR(50) UNIQUE,
    department VARCHAR(100),
    semester INT,
    profile_image LONGBLOB,
    face_encoding LONGBLOB COMMENT 'Stored face encoding for recognition',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_enrollment (enrollment_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- ADMIN TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'super_admin',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- EVENT ORGANISERS TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS event_organisers (
    organiser_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    contact_number VARCHAR(15),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- EVENTS TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS events (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    event_name VARCHAR(200) NOT NULL,
    description TEXT,
    event_date DATE NOT NULL,
    event_time TIME,
    location VARCHAR(200),
    max_capacity INT,
    min_cgpa DECIMAL(3, 2) DEFAULT 0.00 COMMENT 'Minimum CGPA requirement',
    min_attendance DECIMAL(5, 2) DEFAULT 0.00 COMMENT 'Minimum attendance requirement',
    is_paid BOOLEAN DEFAULT FALSE,
    event_fee DECIMAL(10, 2) DEFAULT 0.00,
    organiser_id INT,
    admin_id INT,
    event_status ENUM('upcoming', 'ongoing', 'completed', 'cancelled') DEFAULT 'upcoming',
    banner_image LONGBLOB,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (organiser_id) REFERENCES event_organisers(organiser_id) ON DELETE SET NULL,
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id) ON DELETE SET NULL,
    INDEX idx_event_date (event_date),
    INDEX idx_status (event_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- REGISTRATIONS TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS registrations (
    registration_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registration_status ENUM('registered', 'participated', 'cancelled') DEFAULT 'registered',
    is_eligible BOOLEAN DEFAULT FALSE,
    ineligibility_reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_registration (student_id, event_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_event (event_id),
    INDEX idx_status (registration_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- PAYMENTS TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    registration_id INT NOT NULL,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    razorpay_order_id VARCHAR(100) UNIQUE,
    razorpay_payment_id VARCHAR(100) UNIQUE,
    razorpay_signature VARCHAR(255),
    payment_status ENUM('pending', 'completed', 'failed', 'refunded') DEFAULT 'pending',
    payment_method VARCHAR(50) DEFAULT 'razorpay',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (registration_id) REFERENCES registrations(registration_id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_event (event_id),
    INDEX idx_status (payment_status),
    INDEX idx_razorpay_id (razorpay_payment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- ATTENDANCE TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    registration_id INT NOT NULL,
    attendance_status ENUM('present', 'absent') DEFAULT 'absent',
    check_in_time TIMESTAMP,
    check_out_time TIMESTAMP,
    face_recognition_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_attendance (student_id, event_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (registration_id) REFERENCES registrations(registration_id) ON DELETE CASCADE,
    INDEX idx_event (event_id),
    INDEX idx_status (attendance_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- CERTIFICATES TABLE
-- =============================================
CREATE TABLE IF NOT EXISTS certificates (
    certificate_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    event_id INT NOT NULL,
    registration_id INT NOT NULL,
    certificate_number VARCHAR(100) UNIQUE NOT NULL,
    issue_date DATE,
    certificate_file_path VARCHAR(255),
    certificate_pdf LONGBLOB,
    is_downloaded BOOLEAN DEFAULT FALSE,
    download_count INT DEFAULT 0,
    last_download_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON DELETE CASCADE,
    FOREIGN KEY (registration_id) REFERENCES registrations(registration_id) ON DELETE CASCADE,
    INDEX idx_student (student_id),
    INDEX idx_event (event_id),
    INDEX idx_certificate_number (certificate_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- =============================================
-- CREATE DEFAULT ADMIN USER
-- =============================================
-- Password: admin123 (bcrypt hash)
-- Update this in production with a secure password
INSERT INTO admin (name, email, password_hash, role, is_active) 
VALUES ('Super Admin', 'admin@campus.edu', '$2b$12$zXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', 'super_admin', TRUE)
ON DUPLICATE KEY UPDATE email=email;

-- =============================================
-- CREATE INDEXES FOR PERFORMANCE
-- =============================================
CREATE INDEX idx_event_organiser ON events(organiser_id);
CREATE INDEX idx_registration_event_date ON registrations(event_id, registration_date);
CREATE INDEX idx_payment_date ON payments(transaction_date);
CREATE INDEX idx_attendance_event_date ON attendance(event_id, check_in_time);
