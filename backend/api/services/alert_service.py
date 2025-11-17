# services/alert_service.py
from typing import List, Dict, Any
from django.db.models import QuerySet
from django.utils import timezone
from alerts.models import Alert, AlertChannel
from events.models import Event


class AlertService:
    """Класс сервиса для обработки бизнес-логики, связанной с оповещениями"""
    
    @staticmethod
    def send_alert_to_channels(event_id: int, channel_ids: List[int]) -> List[Dict[str, Any]]:
        """Отправить оповещение о событии в указанные каналы"""
        try:
            event = Event.objects.get(id=event_id)
            channels = AlertChannel.objects.filter(id__in=channel_ids)
            
            sent_alerts = []
            for channel in channels:
                alert = Alert.objects.create(
                    event=event,
                    channel=channel,
                    message=f'Event: {event.object_class} detected at {event.timestamp}'
                )
                sent_alerts.append({
                    'alert_id': alert.id,
                    'channel': channel.name,
                    'status': 'pending'
                })
            
            return sent_alerts
        except Event.DoesNotExist:
            raise ValueError(f"Event with id {event_id} not found")
    
    @staticmethod
    def send_batch_alerts(event_ids: List[int], channel_ids: List[int]) -> List[Dict[str, Any]]:
        """Отправить оповещения о нескольких событиях в несколько каналов"""
        sent_alerts = []
        
        for event_id in event_ids:
            try:
                event = Event.objects.get(id=event_id)
                for channel_id in channel_ids:
                    try:
                        channel = AlertChannel.objects.get(id=channel_id)
                        alert = Alert.objects.create(
                            event=event,
                            channel=channel,
                            message=f'Event: {event.object_class} detected at {event.timestamp}'
                        )
                        sent_alerts.append({
                            'alert_id': alert.id,
                            'event_id': event_id,
                            'channel_id': channel_id,
                            'status': 'pending'
                        })
                    except AlertChannel.DoesNotExist:
                        continue
            except Event.DoesNotExist:
                continue
        
        return sent_alerts
    
    @staticmethod
    def get_alerts_by_event(event_id: int) -> QuerySet[Alert]:
        """Получить все оповещения для определенного события"""
        return Alert.objects.filter(event_id=event_id)
    
    @staticmethod
    def get_alerts_by_channel(channel_id: int) -> QuerySet[Alert]:
        """Получить все оповещения, отправленные в определенный канал"""
        return Alert.objects.filter(channel_id=channel_id)
    
    @staticmethod
    def get_recent_alerts(hours: int = 24) -> QuerySet[Alert]:
        """Получить оповещения за последние N часов"""
        time_threshold = timezone.now() - timezone.timedelta(hours=hours)
        return Alert.objects.filter(created_at__gte=time_threshold).order_by('-created_at')
    
    @staticmethod
    def get_alert_statistics(start_date: Any = None, end_date: Any = None) -> Dict[str, Any]:
        """Получить статистику оповещений для дашборда"""
        queryset = Alert.objects.all()
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        
        stats = {
            'total_alerts': queryset.count(),
            'alerts_by_channel': {},
            'alerts_by_status': {},
            'sent_alerts': queryset.filter(status='sent').count(),
            'pending_alerts': queryset.filter(status='pending').count(),
            'failed_alerts': queryset.filter(status='failed').count(),
        }
        
        # Count alerts by channel
        for alert in queryset:
            channel_name = alert.channel.name
            stats['alerts_by_channel'][channel_name] = stats['alerts_by_channel'].get(channel_name, 0) + 1
            
            status = alert.status
            stats['alerts_by_status'][status] = stats['alerts_by_status'].get(status, 0) + 1
        
        return stats