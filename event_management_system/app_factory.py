"""
Smart Campus Event Management System
Main Flask Application
"""
from flask import Flask, render_template, redirect, url_for, session, request, flash, jsonify
from functools import wraps
from datetime import datetime, timedelta
import os
import sys

# Add utils to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.config import get_config
from utils.database import init_db, get_db_connection
from utils.auth import login_required, role_required


def create_app(config_name='development'):
    """Application factory"""
    
    # Get the path to templates folder
    template_dir = os.path.join(os.path.dirname(__file__), 'app', 'templates')
    static_dir = os.path.join(os.path.dirname(__file__), 'app', 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Load configuration
    app.config.from_object(get_config(config_name))
    
    # Initialize database
    init_db(app)
    
    # Session configuration
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    
    # Register blueprint routes
    from app.routes import student_routes, admin_routes, organiser_routes, auth_routes
    
    app.register_blueprint(auth_routes.auth_bp)
    app.register_blueprint(student_routes.student_bp)
    app.register_blueprint(admin_routes.admin_bp)
    app.register_blueprint(organiser_routes.organiser_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors"""
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors"""
        return render_template('errors/403.html'), 403
    
    # Context processor for user info
    @app.context_processor
    def inject_user():
        """Inject user info into templates"""
        user_info = {
            'student_id': session.get('student_id'),
            'admin_id': session.get('admin_id'),
            'organiser_id': session.get('organiser_id'),
            'user_type': session.get('user_type'),
            'user_name': session.get('user_name'),
            'role': session.get('role')
        }
        return dict(user=user_info)
    
    # Before request handler
    @app.before_request
    def before_request():
        """Update session last activity time"""
        session.permanent = True
        app.permanent_session_lifetime = timedelta(seconds=app.config['SESSION_TIMEOUT'])
        session.modified = True
    
    # Home page route
    @app.route('/')
    def index():
        """Home page"""
        if 'student_id' in session:
            return redirect(url_for('student.dashboard'))
        elif 'admin_id' in session:
            return redirect(url_for('admin.dashboard'))
        elif 'organiser_id' in session:
            return redirect(url_for('organiser.dashboard'))
        
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        """Redirect to appropriate dashboard"""
        if 'student_id' in session:
            return redirect(url_for('student.dashboard'))
        elif 'admin_id' in session:
            return redirect(url_for('admin.dashboard'))
        elif 'organiser_id' in session:
            return redirect(url_for('organiser.dashboard'))
        
        flash('Please log in first', 'warning')
        return redirect(url_for('auth.login'))
    
    @app.route('/logout')
    def logout():
        """Logout user"""
        session.clear()
        flash('You have been logged out successfully', 'success')
        return redirect(url_for('index'))
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
