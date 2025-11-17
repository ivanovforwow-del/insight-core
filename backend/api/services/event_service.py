# services/event_service.py
from typing import List, Dict, Any, Optional
from django.utils import timezone
from django.db.models import QuerySet
from datetime import datetime, timedelta
from events.models import Event, Rule
from cameras.models import Camera
from alerts.models import Alert


class EventService:
    """Класс сервиса для обработки бизнес-логики, связанной с событиями"""
    
    @staticmethod
    def get_events_for_time_range(start_date: Optional[datetime] = None, 
                                end_date: Optional[datetime] = None) -> QuerySet[Event]:
        """Получить события, отфильтрованные по временному диапазону"""
        queryset = Event.objects.all()
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        return queryset
    
    @staticmethod
    def get_events_by_camera(camera_id: int) -> QuerySet[Event]:
        """Получить события для определенной камеры"""
        return Event.objects.filter(camera_id=camera_id).order_by('-timestamp')
    
    @staticmethod
    def get_events_by_rule(rule_id: int) -> QuerySet[Event]:
        """Получить события для определенного правила"""
        return Event.objects.filter(rule_id=rule_id).order_by('-timestamp')
    
    @staticmethod
    def get_recent_events(hours: int = 24) -> QuerySet[Event]:
        """Получить события за последние N часов"""
        time_threshold = timezone.now() - timedelta(hours=hours)
        return Event.objects.filter(timestamp__gte=time_threshold).order_by('-timestamp')
    
    @staticmethod
    def get_events_by_type(object_class: str) -> QuerySet[Event]:
        """Получить события, отфильтрованные по классу объекта"""
        return Event.objects.filter(object_class=object_class).order_by('-timestamp')
    
    @staticmethod
    def resolve_event(event_id: int, resolver_user: Any) -> Event:
        """Отметить событие как решенное"""
        event = Event.objects.get(id=event_id)
        event.resolved = True
        event.resolved_at = timezone.now()
        event.resolved_by = resolver_user
        event.save()
        return event
    
    @staticmethod
    def create_alerts_for_event(event: Event, channel_ids: List[int]) -> List[Alert]:
        """Создать оповещения для события"""
        from alerts.models import AlertChannel
        channels = AlertChannel.objects.filter(id__in=channel_ids)
        
        alerts = []
        for channel in channels:
            alert = Alert.objects.create(
                event=event,
                channel=channel,
                message=f'Event: {event.object_class} detected at {event.timestamp}'
            )
            alerts.append(alert)
        
        return alerts
    
    @staticmethod
    def get_event_statistics(start_date: Optional[datetime] = None, 
                           end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Получить статистику событий для дашборда"""
        events = EventService.get_events_for_time_range(start_date, end_date)
        
        stats = {
            'total_events': events.count(),
            'events_by_type': {},
            'events_by_camera': {},
            'resolved_events': events.filter(resolved=True).count(),
            'unresolved_events': events.filter(resolved=False).count(),
        }
        
        # Count events by type
        for event in events:
            object_class = event.object_class
            stats['events_by_type'][object_class] = stats['events_by_type'].get(object_class, 0) + 1
            
            camera_name = event.camera.name
            stats['events_by_camera'][camera_name] = stats['events_by_camera'].get(camera_name, 0) + 1
        
        return stats