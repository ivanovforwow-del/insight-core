# services/camera_service.py
from typing import List, Optional, Dict, Any
from django.db.models import QuerySet
from django.contrib.auth.models import User
from cameras.models import Camera, Zone, Line
from events.models import Rule
from videos.models import VideoFile
from events.models import Event


class CameraService:
    """Service class for handling camera-related business logic"""
    
    @staticmethod
    def get_cameras_with_stats(user: User) -> List[Dict[str, Any]]:
        """Get cameras with statistics for dashboard"""
        cameras = Camera.objects.all()
        camera_data = []
        
        for camera in cameras:
            # Get events count for last 24 hours
            events_count = Event.objects.filter(
                camera=camera,
                timestamp__gte=Event.objects.datetimes('timestamp', 'hour')[0] - Event.objects.datetimes('timestamp', 'hour').model.timedelta(hours=24)
            ).count()
            
            # Get last event
            last_event = Event.objects.filter(camera=camera).order_by('-timestamp').first()
            
            camera_info = {
                'id': camera.id,
                'name': camera.name,
                'status': camera.status,
                'location': camera.location,
                'events_count': events_count,
                'last_event': last_event.timestamp if last_event else None
            }
            camera_data.append(camera_info)
        
        return camera_data
    
    @staticmethod
    def get_camera_zones(camera_id: int) -> QuerySet[Zone]:
        """Get zones for specific camera"""
        return Zone.objects.filter(camera_id=camera_id)
    
    @staticmethod
    def get_camera_lines(camera_id: int) -> QuerySet[Line]:
        """Get lines for specific camera"""
        return Line.objects.filter(camera_id=camera_id)
    
    @staticmethod
    def get_camera_rules(camera_id: int) -> QuerySet[Rule]:
        """Get rules for specific camera"""
        return Rule.objects.filter(camera=camera_id)
    
    @staticmethod
    def get_camera_events(camera_id: int) -> QuerySet[Event]:
        """Get events for specific camera"""
        return Event.objects.filter(camera_id=camera_id).order_by('-timestamp')
    
    @staticmethod
    def get_camera_video_files(camera_id: int) -> QuerySet[VideoFile]:
        """Get video files for specific camera"""
        return VideoFile.objects.filter(camera_id=camera_id).order_by('-start_time')
    
    @staticmethod
    def update_camera_config(camera_id: int, config_data: Dict[str, Any]) -> Camera:
        """Update camera configuration"""
        camera = Camera.objects.get(id=camera_id)
        for field, value in config_data.items():
            if hasattr(camera, field):
                setattr(camera, field, value)
        camera.save()
        return camera