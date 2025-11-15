# views/alert_views.py
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from alerts.models import Alert, AlertChannel
from ..serializers.alert_serializers import AlertSerializer, AlertChannelSerializer
from ..services.alert_service import AlertService


class AlertChannelViewSet(viewsets.ModelViewSet):
    queryset = AlertChannel.objects.all()
    serializer_class = AlertChannelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['channel_type', 'enabled']
    search_fields = ['name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['event', 'channel', 'status', 'sent_at']
    search_fields = ['message']
    ordering_fields = ['created_at', 'sent_at']
    ordering = ['-created_at']


# Alert Management Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendAlertView(request):
    """Отправка алерта"""
    event_id = request.data.get('event_id')
    channel_ids = request.data.get('channel_ids', [])
    
    if not event_id or not channel_ids:
        return Response({'error': 'Event ID and channel IDs are required'}, status=400)
    
    try:
        sent_alerts = AlertService.send_alert_to_channels(event_id, channel_ids)
        return Response({'sent_alerts': sent_alerts})
    except ValueError as e:
        return Response({'error': str(e)}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def BatchAlertView(request):
    """Массовая отправка алертов"""
    event_ids = request.data.get('event_ids', [])
    channel_ids = request.data.get('channel_ids', [])
    
    if not event_ids or not channel_ids:
        return Response({'error': 'Event IDs and channel IDs are required'}, status=400)
    
    sent_alerts = AlertService.send_batch_alerts(event_ids, channel_ids)
    return Response({'sent_alerts': sent_alerts})