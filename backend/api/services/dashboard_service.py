# services/dashboard_service.py
from typing import Dict, Any
from django.utils import timezone
from events.models import Event
from cameras.models import Camera
from alerts.models import Alert
from videos.models import VideoFile
from .event_service import EventService
from .camera_service import CameraService
from .analytics_service import AnalyticsService


class DashboardService:
    """Service class for handling dashboard-related business logic"""
    
    @staticmethod
    def get_dashboard_stats() -> Dict[str, Any]:
        """Get comprehensive dashboard statistics"""
        today = timezone.now().date()
        
        stats = {
            'total_cameras': Camera.objects.filter(status='active').count(),
            'total_events_today': Event.objects.filter(timestamp__date=today).count(),
            'total_alerts_today': Alert.objects.filter(created_at__date=today).count(),
            'total_videos_today': VideoFile.objects.filter(created_at__date=today).count(),
            'recent_events': list(EventService.get_recent_events(hours=24)[:10].values())
        }
        return stats
    
    @staticmethod
    def get_dashboard_events() -> Dict[str, Any]:
        """Get events data for dashboard"""
        events = EventService.get_recent_events(hours=24)[:50]
        result = {
            'events': list(events.values()),  # This would use serializers in real implementation
            'total_count': events.count()
        }
        return result
    
    @staticmethod
    def get_dashboard_cameras() -> Dict[str, Any]:
        """Get cameras data for dashboard with statistics"""
        return {
            'cameras_data': CameraService.get_cameras_with_stats(None)  # User parameter would be handled in view
        }