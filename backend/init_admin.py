#!/usr/bin/env python
"""
Script to create or update admin user with known password
This script ensures that an admin user exists with predictable credentials
for development and testing purposes.
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings_docker')

django.setup()

# Import User model AFTER Django setup
from django.contrib.auth.models import User

def create_or_update_admin():
    """Create or update admin user with known password"""
    admin_username = 'admin'
    admin_password = 'admin123'
    
    # Check if admin user exists
    try:
        admin_user = User.objects.get(username=admin_username)
        print(f'Admin user "{admin_username}" already exists, updating password...')
    except User.DoesNotExist:
        print(f'Creating admin user "{admin_username}"...')
        admin_user = User.objects.create_superuser(
            username=admin_username,
            email='admin@insightcore.com',
            password=admin_password
        )
    
    # Set password anyway to ensure it's correct
    admin_user.set_password(admin_password)
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    
    print(f'Admin user "{admin_username}" is ready with password "{admin_password}"')
    print('Please change this password in production environments!')

if __name__ == '__main__':
    create_or_update_admin()