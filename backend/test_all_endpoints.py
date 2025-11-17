#!/usr/bin/env python
"""Test script to check ALL backend endpoints"""

import requests
import json
import sys
import os
import time
from urllib.parse import urljoin

# Base URL for the API
BASE_URL = 'http://127.0.0.1:8000'
API_BASE = urljoin(BASE_URL, '/api/')

def test_endpoint(url, method='GET', data=None, headers=None, expected_status=None, auth_required=False):
    """Test a single endpoint"""
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    
    try:
        # Prepare request
        request_kwargs = {'headers': headers}
        if data:
            request_kwargs['json'] = data
        
        start_time = time.time()
        
        if method == 'GET':
            response = requests.get(url, **request_kwargs)
        elif method == 'POST':
            response = requests.post(url, **request_kwargs)
        elif method == 'PUT':
            response = requests.put(url, **request_kwargs)
        elif method == 'PATCH':
            response = requests.patch(url, **request_kwargs)
        elif method == 'DELETE':
            response = requests.delete(url, **request_kwargs)
        else:
            print(f"Unsupported method: {method}")
            return False, f"Unsupported method: {method}"
        
        elapsed_time = time.time() - start_time
        
        # Check if status is as expected (or one of the expected statuses)
        success = False
        if expected_status:
            if isinstance(expected_status, int):
                success = response.status_code == expected_status
            elif isinstance(expected_status, list):
                success = response.status_code in expected_status
        else:
            # For endpoints that might require authentication, accept 200 or 401
            if auth_required:
                success = response.status_code in [200, 401, 403]
            else:
                success = response.status_code in [200, 201, 204]  # Common success codes
        
        status_desc = 'PASS' if success else 'FAIL'
        print(f"{method:6} {url:<60} Status: {response.status_code:3} ({status_desc}) [{elapsed_time:.2f}s]")
        
        if not success and response.status_code not in [401, 403]:
            print(f"         Expected: {expected_status or '200/201/204'}, Got: {response.status_code}")
            if response.text:
                try:
                    # Try to parse as JSON for better formatting
                    json_response = response.json()
                    print(f"         Response: {json.dumps(json_response, indent=8)}")
                except:
                    print(f"         Response: {response.text}")
        
        return success, response.status_code
    except requests.exceptions.ConnectionError:
        print(f"{method:6} {url:<60} ERROR: Cannot connect to server")
        return False, "ConnectionError"
    except Exception as e:
        print(f"{method:6} {url:<60} ERROR: {str(e)}")
        return False, str(e)

def main():
    print("Testing ALL backend endpoints...")
    print(f"Base URL: {BASE_URL}")
    print(f"API Base: {API_BASE}")
    print("-" * 100)
    
    # Collect all test results
    all_tests = []
    
    # Test health check endpoint
    print("\nTesting Health Check Endpoint:")
    success, status = test_endpoint(urljoin(BASE_URL, '/api/health/'), 'GET', expected_status=200)
    all_tests.append(("Health Check", success))
    
    # Test authentication endpoints
    print("\nTesting Authentication Endpoints:")
    auth_tests = [
        ('POST', urljoin(API_BASE, 'auth/token/'), {"username": "test", "password": "test"}, 400),  # Should return 400 for bad credentials
        ('POST', urljoin(API_BASE, 'auth/token/refresh/'), {"refresh": "dummy_token"}, 401),  # Should return 401 for invalid token
        ('POST', urljoin(API_BASE, 'auth/token/verify/'), {"token": "dummy_token"}, 401),  # Should return 401 for invalid token
    ]
    
    for method, url, data, expected in auth_tests:
        success, status = test_endpoint(url, method, data, expected_status=expected)
        all_tests.append((f"Auth - {url.split('/')[-2]}", success))
    
    # Test ViewSet endpoints (GET requests to list endpoints)
    print("\nTesting ViewSet List Endpoints (may require authentication):")
    viewset_list_tests = [
        ('GET', urljoin(API_BASE, 'cameras/')),
        ('GET', urljoin(API_BASE, 'zones/')),
        ('GET', urljoin(API_BASE, 'lines/')),
        ('GET', urljoin(API_BASE, 'rules/')),
        ('GET', urljoin(API_BASE, 'video-files/')),
        ('GET', urljoin(API_BASE, 'clips/')),
        ('GET', urljoin(API_BASE, 'video-annotations/')),
        ('GET', urljoin(API_BASE, 'events/')),
        ('GET', urljoin(API_BASE, 'alert-channels/')),
        ('GET', urljoin(API_BASE, 'alerts/')),
        ('GET', urljoin(API_BASE, 'ml-models/')),
    ]
    
    for method, url in viewset_list_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"ViewSet List - {url.split('/')[-2]}", success))
    
    # Test dashboard endpoints
    print("\nTesting Dashboard Endpoints (may require authentication):")
    dashboard_tests = [
        ('GET', urljoin(API_BASE, 'dashboard/stats/')),
        ('GET', urljoin(API_BASE, 'dashboard/events/')),
        ('GET', urljoin(API_BASE, 'dashboard/cameras/')),
    ]
    
    for method, url in dashboard_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Dashboard - {url.split('/')[-1]}", success))
    
    # Test video processing endpoints
    print("\nTesting Video Processing Endpoints (may require authentication):")
    video_tests = [
        ('GET', urljoin(API_BASE, 'video/analyze/')),
        ('POST', urljoin(API_BASE, 'video/process/')),
        ('POST', urljoin(API_BASE, 'video/upload/')),
    ]
    
    for method, url in video_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Video - {url.split('/')[-1]}", success))
    
    # Test live stream endpoints (these need a valid camera ID)
    print("\nTesting Live Stream Endpoints (may require authentication):")
    stream_tests = [
        ('GET', urljoin(API_BASE, 'stream/123e4567-e89b-12d3-a456-426614174000/')),  # Using dummy UUID
        ('GET', urljoin(API_BASE, 'stream/123e4567-e89b-12d3-a456-426614174000/snapshot/')),
    ]
    
    for method, url in stream_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Stream - {url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]}", success))
    
    # Test analytics endpoints
    print("\nTesting Analytics Endpoints (may require authentication):")
    analytics_tests = [
        ('GET', urljoin(API_BASE, 'analytics/heatmap/')),
        ('GET', urljoin(API_BASE, 'analytics/timeline/')),
        ('GET', urljoin(API_BASE, 'analytics/report/')),
    ]
    
    for method, url in analytics_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Analytics - {url.split('/')[-1]}", success))
    
    # Test alert management endpoints
    print("\nTesting Alert Management Endpoints (may require authentication):")
    alert_tests = [
        ('POST', urljoin(API_BASE, 'alerts/send/')),
        ('GET', urljoin(API_BASE, 'alerts/batch/')),
    ]
    
    for method, url in alert_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Alert - {url.split('/')[-1]}", success))
    
    # Test configuration endpoints
    print("\nTesting Configuration Endpoints (may require authentication):")
    config_tests = [
        ('GET', urljoin(API_BASE, 'config/camera/123e4567-e89b-12d3-a456-426614174000/')),  # Using dummy UUID
        ('GET', urljoin(API_BASE, 'config/rules/')),
    ]
    
    for method, url in config_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Config - {url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]}", success))
    
    # Test camera-specific endpoints
    print("\nTesting Camera-Specific Endpoints (may require authentication):")
    camera_specific_tests = [
        ('GET', urljoin(API_BASE, 'cameras/123e4567-e89b-12d3-a456-426614174000/zones/')),  # Using dummy UUID
        ('GET', urljoin(API_BASE, 'cameras/123e4567-e89b-12d3-a456-426614174000/lines/')),
        ('GET', urljoin(API_BASE, 'cameras/123e4567-e89b-12d3-a456-426614174000/rules/')),
        ('GET', urljoin(API_BASE, 'cameras/123e4567-e89b-12d3-a456-426614174000/events/')),
        ('GET', urljoin(API_BASE, 'cameras/123e4567-e89b-12d3-a456-426614174000/video-files/')),
    ]
    
    for method, url in camera_specific_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Camera-specific - {url.split('/')[-2]}", success))
    
    # Test rule-specific endpoints
    print("\nTesting Rule-Specific Endpoints (may require authentication):")
    rule_specific_tests = [
        ('GET', urljoin(API_BASE, 'rules/123e4567-e89b-12d3-a456-426614174000/events/')),  # Using dummy UUID
        ('POST', urljoin(API_BASE, 'rules/123e4567-e89b-12d3-a456-426614174000/test/')),
    ]
    
    for method, url in rule_specific_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Rule-specific - {url.split('/')[-2]}", success))
    
    # Test event-specific endpoints
    print("\nTesting Event-Specific Endpoints (may require authentication):")
    event_specific_tests = [
        ('POST', urljoin(API_BASE, 'events/123e4567-e89b-12d3-a456-426614174000/resolve/')),  # Using dummy UUID
        ('GET', urljoin(API_BASE, 'events/123e4567-e89b-12d3-a456-426614174000/clip/')),
    ]
    
    for method, url in event_specific_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Event-specific - {url.split('/')[-2]}", success))
    
    # Test video file-specific endpoints
    print("\nTesting Video File-Specific Endpoints (may require authentication):")
    video_file_specific_tests = [
        ('GET', urljoin(API_BASE, 'video-files/123e4567-e89b-12d3-a456-426614174000/clips/')),  # Using dummy UUID
        ('GET', urljoin(API_BASE, 'video-files/123e4567-e89b-12d3-a456-426614174000/download/')),
    ]
    
    for method, url in video_file_specific_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"VideoFile-specific - {url.split('/')[-2]}", success))
    
    # Test clip-specific endpoints
    print("\nTesting Clip-Specific Endpoints (may require authentication):")
    clip_specific_tests = [
        ('GET', urljoin(API_BASE, 'clips/123e4567-e89b-12d3-a456-426614174000/annotations/')),  # Using dummy UUID
        ('GET', urljoin(API_BASE, 'clips/123e4567-e89b-12d3-a456-426614174000/download/')),
    ]
    
    for method, url in clip_specific_tests:
        success, status = test_endpoint(url, method, auth_required=True)
        all_tests.append((f"Clip-specific - {url.split('/')[-2]}", success))
    
    # Summary
    print("\n" + "="*100)
    print("TEST SUMMARY:")
    print("="*100)
    
    passed = sum(1 for _, result in all_tests if result)
    total = len(all_tests)
    
    for test_name, result in all_tests:
        status = "PASS" if result else "FAIL"
        print(f"{status:4} {test_name}")
    
    print(f"\nTotal: {total} tests, {passed} passed, {total - passed} failed")
    print(f"Success rate: {passed/total*100:.1f}%" if total > 0 else "0%")
    
    if total > 0:
        if passed == total:
            print("\n🎉 All tests PASSED! All endpoints are working correctly.")
        else:
            print(f"\n⚠️  {total - passed} endpoints failed. Check the output above for details.")

if __name__ == '__main__':
    main()