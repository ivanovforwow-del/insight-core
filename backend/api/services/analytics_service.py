# services/analytics_service.py
from typing import Dict, Any, Optional, List
from django.db.models import QuerySet
from django.utils import timezone
from datetime import datetime
from events.models import Event
from alerts.models import Alert
from cameras.models import Camera


class AnalyticsService:
    """Service class for handling analytics and reporting business logic"""
    
    @staticmethod
    def get_heatmap_data(camera_id: Optional[int] = None, 
                        start_date: Optional[datetime] = None, 
                        end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Generate heatmap data for events"""
        queryset = Event.objects.all()
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        # Placeholder for heatmap data generation
        # In real implementation, this would generate spatial data for heatmap
        result = {
            'heatmap_data': [],
            'camera_id': camera_id,
            'date_range': {'start': start_date, 'end': end_date}
        }
        return result
    
    @staticmethod
    def get_timeline_data(camera_id: Optional[int] = None,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Generate timeline data for events"""
        queryset = Event.objects.all()
        if camera_id:
            queryset = queryset.filter(camera_id=camera_id)
        if start_date:
            queryset = queryset.filter(timestamp__range=[start_date, end_date])
        else:
            queryset = queryset.order_by('-timestamp')
        
        events = queryset[:100]  # Limit to 100 events for performance
        result = {
            'events': list(events.values()),  # This would use serializers in real implementation
            'total_count': events.count()
        }
        return result
    
    @staticmethod
    def get_analytics_report(start_date: Optional[datetime] = None,
                           end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        events_queryset = Event.objects.all()
        alerts_queryset = Alert.objects.all()
        
        if start_date and end_date:
            events_queryset = events_queryset.filter(timestamp__range=[start_date, end_date])
            alerts_queryset = alerts_queryset.filter(created_at__range=[start_date, end_date])
        
        # Count events by type
        events_by_type = {}
        events_by_camera = {}
        
        for event in events_queryset:
            # Count by type
            obj_class = event.object_class
            events_by_type[obj_class] = events_by_type.get(obj_class, 0) + 1
            
            # Count by camera
            camera_name = event.camera.name
            events_by_camera[camera_name] = events_by_camera.get(camera_name, 0) + 1
        
        result = {
            'report_data': {
                'total_events': events_queryset.count(),
                'events_by_type': events_by_type,
                'events_by_camera': events_by_camera,
                'alerts_sent': alerts_queryset.count(),
                'resolved_events': events_queryset.filter(resolved=True).count(),
                'unresolved_events': events_queryset.filter(resolved=False).count(),
                'events_by_severity': AnalyticsService._get_events_by_severity(events_queryset)
            }
        }
        return result
    
    @staticmethod
    def _get_events_by_severity(queryset: QuerySet[Event]) -> Dict[str, int]:
        """Helper method to count events by severity"""
        severity_counts = {}
        for event in queryset:
            severity = event.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        return severity_counts
    
    @staticmethod
    def get_dashboard_stats() -> Dict[str, Any]:
        """Get dashboard statistics"""
        from django.db.models import Count, Avg
        
        today = timezone.now().date()
        
        stats = {
            'total_cameras': Camera.objects.filter(status='active').count(),
            'total_events_today': Event.objects.filter(timestamp__date=today).count(),
            'total_alerts_today': Alert.objects.filter(created_at__date=today).count(),
            'total_videos_today': Event.objects.filter(timestamp__date=today).count(),  # Assuming events are related to videos
            'recent_events': list(Event.objects.filter(
                timestamp__gte=timezone.now() - timezone.timedelta(hours=24)
            )[:10].values())  # This would use serializers in real implementation
        }
        return stats