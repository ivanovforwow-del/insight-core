#!/usr/bin/env python
"""Test script to check backend endpoints"""

import requests
import json
import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Base URL for the API
BASE_URL = 'http://localhost:8000'

def test_endpoint(url, method='GET', data=None, headers=None, expected_status=200):
    """Test a single endpoint"""
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            print(f"Unsupported method: {method}")
            return False
        
        success = response.status_code == expected_status
        print(f"{method} {url} - Status: {response.status_code} ({'PASS' if success else 'FAIL'})")
        
        if not success:
            print(f"  Expected: {expected_status}, Got: {response.status_code}")
            if response.text:
                print(f"  Response: {response.text}")
        
        return success
    except Exception as e:
        print(f"{method} {url} - ERROR: {str(e)}")
        return False

def main():
    print("Testing backend endpoints...")
    
    # Test authentication endpoints
    auth_tests = [
        ('GET', f'{BASE_URL}/api/auth/user/', None, 401),  # Should require auth
    ]
    
    print("\nTesting Authentication Endpoints:")
    for method, url, data, expected in auth_tests:
        test_endpoint(url, method, data, expected_status=expected)
    
    # Test API endpoints (these may require authentication)
    api_tests = [
        ('GET', f'{BASE_URL}/api/cameras/', None, 200),
        ('GET', f'{BASE_URL}/api/events/', None, 200),
        ('GET', f'{BASE_URL}/api/alerts/', None, 200),
        ('GET', f'{BASE_URL}/api/analytics/', None, 200),
    ]
    
    print("\nTesting API Endpoints (may require authentication):")
    for method, url, data, expected in api_tests:
        test_endpoint(url, method, data, expected_status=expected)
    
    # Test basic endpoints
    basic_tests = [
        ('GET', f'{BASE_URL}/', None, 200),
        ('GET', f'{BASE_URL}/health/', None, 200),
    ]
    
    print("\nTesting Basic Endpoints:")
    for method, url, data, expected in basic_tests:
        test_endpoint(url, method, data, expected_status=expected)
    
    print("\nTesting complete.")

if __name__ == '__main__':
    main()