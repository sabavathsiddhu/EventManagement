import os
import sys

# Add the event_management_system directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'event_management_system'))

from app_factory import create_app

# Render needs an initialized app instance to serve as the WSGI application
app = create_app('production')
