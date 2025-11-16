# views/event_views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta

from events.models import Event, Rule
from ..serializers.event_serializers import EventSerializer
from ..serializers.camera_serializers import RuleSerializer
from ..services.event_service import EventService


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['camera', 'rule_type', 'severity', 'enabled']
    search_fields = ['name', 'description', 'camera__name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['camera', 'rule', 'object_class', 'severity', 'resolved', 'timestamp']
    search_fields = ['object_class', 'track_id']
    ordering_fields = ['timestamp', 'created_at']
    ordering = ['-timestamp']

    def get_queryset(self):
        # Добавим возможность фильтрации по времени
        queryset = Event.objects.all()
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        return queryset


# Event-specific Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EventResolveView(request, pk):
    """Разрешение события"""
    try:
        resolved_event = EventService.resolve_event(pk, request.user)
        serializer = EventSerializer(resolved_event)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def EventClipView(request, pk):
    """Клип для события"""
    try:
        event = Event.objects.get(id=pk)
        if event.clip:
            from ..serializers.video_serializers import ClipSerializer
            serializer = ClipSerializer(event.clip)
            return Response(serializer.data)
        else:
            return Response({'error': 'No clip available for this event'}, status=status.HTTP_404_NOT_FOUND)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RuleEventsView(request, pk):
    """События для конкретного правила"""
    try:
        events = EventService.get_events_by_rule(pk)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RuleTestView(request, pk):
    """Тестирование правила"""
    try:
        from events.models import Rule
        rule = Rule.objects.get(id=pk)
        # Здесь будет реализована логика тестирования правила
        result = {
            'rule_id': pk,
            'rule_name': rule.name,
            'test_result': 'passed',  # или 'failed'
            'conditions': rule.conditions
        }
        return Response(result)
    except Rule.DoesNotExist:
        return Response({'error': 'Rule not found'}, status=status.HTTP_404_NOT_FOUND)