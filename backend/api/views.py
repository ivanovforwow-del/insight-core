from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json

from cameras.models import Camera, Zone, Line
from videos.models import VideoFile, Clip, VideoAnnotation
from events.models import Rule, Event
from alerts.models import AlertChannel, Alert
from analytics.models import MLModel

from .serializers import (
    CameraSerializer, ZoneSerializer, LineSerializer,
    VideoFileSerializer, ClipSerializer, VideoAnnotationSerializer,
    RuleSerializer, EventSerializer, AlertChannelSerializer, AlertSerializer,
    MLModelSerializer, UserSerializer
)


class MLModelViewSet(viewsets.ModelViewSet):
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'version']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'updated_at', 'accuracy']
    ordering = ['-created_at']


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'vendor']
    search_fields = ['name', 'location', 'rtsp_url']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['camera', 'zone_type', 'is_active']
    search_fields = ['name', 'camera__name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class LineViewSet(viewsets.ModelViewSet):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['camera', 'direction', 'is_active']
    search_fields = ['name', 'camera__name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['camera', 'rule_type', 'severity', 'enabled']
    search_fields = ['name', 'description', 'camera__name']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


class VideoFileViewSet(viewsets.ModelViewSet):
    queryset = VideoFile.objects.all()
    serializer_class = VideoFileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['camera', 'start_time', 'end_time']
    search_fields = ['id', 'storage_path']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['-start_time']


class ClipViewSet(viewsets.ModelViewSet):
    queryset = Clip.objects.all()
    serializer_class = ClipSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['video_file', 'is_annotated']
    search_fields = ['label', 'download_url']
    ordering_fields = ['created_at', 'start_offset']
    ordering = ['-created_at']


class VideoAnnotationViewSet(viewsets.ModelViewSet):
    queryset = VideoAnnotation.objects.all()
    serializer_class = VideoAnnotationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['clip', 'label', 'status', 'created_by']
    search_fields = ['label', 'clip__id']
    ordering_fields = ['created_at', 'start_time']
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


# Custom Token Views
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


class CustomTokenRefreshView(TokenRefreshView):
    pass


class CustomTokenVerifyView(TokenVerifyView):
    pass


# Dashboard Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def DashboardStatsView(request):
    """Статистика для дашборда"""
    from django.db.models import Count, Avg
    
    stats = {
        'total_cameras': Camera.objects.filter(status='active').count(),
        'total_events_today': Event.objects.filter(
            timestamp__date=timezone.now().date()
        ).count(),
        'total_alerts_today': Alert.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
        'total_videos_today': VideoFile.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
        'recent_events': EventSerializer(
            Event.objects.filter(timestamp__gte=timezone.now() - timedelta(hours=24))[:10],
            many=True
        ).data
    }
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def DashboardEventsView(request):
    """События для дашборда"""
    events = Event.objects.filter(
        timestamp__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-timestamp')[:50]
    
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def DashboardCamerasView(request):
    """Камеры для дашборда"""
    cameras = Camera.objects.all()
    data = []
    
    for camera in cameras:
        camera_data = {
            'id': camera.id,
            'name': camera.name,
            'status': camera.status,
            'location': camera.location,
            'events_count': Event.objects.filter(
                camera=camera,
                timestamp__gte=timezone.now() - timedelta(hours=24)
            ).count(),
            'last_event': EventSerializer(
                Event.objects.filter(camera=camera).order_by('-timestamp').first()
            ).data if Event.objects.filter(camera=camera).exists() else None
        }
        data.append(camera_data)
    
    return Response(data)


# Video Processing Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def VideoAnalysisView(request):
    """Анализ видео файла"""
    video_id = request.data.get('video_id')
    if not video_id:
        return Response({'error': 'Video ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        video_file = VideoFile.objects.get(id=video_id)
        # Здесь будет реализована логика анализа видео
        # Пока возвращаем заглушку
        result = {
            'video_id': video_id,
            'status': 'processing',
            'estimated_time': '30 seconds',
            'analysis_type': 'object_detection'
        }
        return Response(result)
    except VideoFile.DoesNotExist:
        return Response({'error': 'Video file not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def VideoProcessView(request):
    """Обработка видео файла"""
    # Здесь будет реализована логика обработки видео
    video_file = request.FILES.get('video')
    if not video_file:
        return Response({'error': 'Video file is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Возвращаем заглушку
    result = {
        'status': 'processing',
        'file_size': video_file.size,
        'file_name': video_file.name,
        'estimated_time': '60 seconds'
    }
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def VideoUploadView(request):
    """Загрузка видео файла"""
    video_file = request.FILES.get('video')
    camera_id = request.data.get('camera_id')
    
    if not video_file or not camera_id:
        return Response({'error': 'Video file and camera ID are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        camera = Camera.objects.get(id=camera_id)
        # Здесь будет реализована логика сохранения видео в MinIO
        # Пока возвращаем заглушку
        result = {
            'status': 'uploaded',
            'file_name': video_file.name,
            'file_size': video_file.size,
            'camera': camera.name
        }
        return Response(result)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


# Live Stream Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def LiveStreamView(request, camera_id):
    """Потоковое видео с камеры"""
    try:
        camera = Camera.objects.get(id=camera_id)
        # Здесь будет реализована логика потокового видео
        result = {
            'camera_id': camera_id,
            'stream_url': camera.rtsp_url,
            'status': camera.status,
            'name': camera.name
        }
        return Response(result)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SnapshotView(request, camera_id):
    """Снимок с камеры"""
    try:
        camera = Camera.objects.get(id=camera_id)
        # Здесь будет реализована логика получения снимка
        result = {
            'camera_id': camera_id,
            'snapshot_url': camera.snapshot.url if camera.snapshot else None,
            'timestamp': timezone.now(),
            'status': camera.status
        }
        return Response(result)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


# Analytics Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def HeatmapView(request):
    """Тепловая карта событий"""
    camera_id = request.query_params.get('camera_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    # Здесь будет реализована логика генерации тепловой карты
    result = {
        'heatmap_data': [],
        'camera_id': camera_id,
        'date_range': {'start': start_date, 'end': end_date}
    }
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def TimelineView(request):
    """Временная шкала событий"""
    camera_id = request.query_params.get('camera_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    events = Event.objects.filter(
        camera_id=camera_id,
        timestamp__range=[start_date, end_date]
    ).order_by('timestamp') if camera_id and start_date and end_date else Event.objects.all().order_by('-timestamp')
    
    result = {
        'events': EventSerializer(events[:100], many=True).data,
        'total_count': events.count()
    }
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AnalyticsReportView(request):
    """Отчет по аналитике"""
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    # Здесь будет реализована логика генерации отчета
    result = {
        'report_data': {
            'total_events': Event.objects.filter(
                timestamp__range=[start_date, end_date]
            ).count() if start_date and end_date else Event.objects.count(),
            'events_by_type': {},
            'events_by_camera': {},
            'alerts_sent': Alert.objects.filter(
                created_at__range=[start_date, end_date]
            ).count() if start_date and end_date else Alert.objects.count()
        }
    }
    return Response(result)


# Alert Management Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendAlertView(request):
    """Отправка алерта"""
    event_id = request.data.get('event_id')
    channel_ids = request.data.get('channel_ids', [])
    
    if not event_id or not channel_ids:
        return Response({'error': 'Event ID and channel IDs are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        event = Event.objects.get(id=event_id)
        channels = AlertChannel.objects.filter(id__in=channel_ids)
        
        # Здесь будет реализована логика отправки алертов
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
        
        return Response({'sent_alerts': sent_alerts})
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def BatchAlertView(request):
    """Массовая отправка алертов"""
    event_ids = request.data.get('event_ids', [])
    channel_ids = request.data.get('channel_ids', [])
    
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
    
    return Response({'sent_alerts': sent_alerts})


# Configuration Views
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def CameraConfigView(request, camera_id):
    """Конфигурация камеры"""
    try:
        camera = Camera.objects.get(id=camera_id)
        if request.method == 'GET':
            serializer = CameraSerializer(camera)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CameraSerializer(camera, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def RulesConfigView(request):
    """Конфигурация правил"""
    if request.method == 'GET':
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        return Response(serializer.data)
    elif request.method == 'PUT':
        # Здесь будет реализована логика обновления правил
        return Response({'status': 'rules updated'})


# Camera-specific Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraZonesView(request, pk):
    """Зоны для конкретной камеры"""
    try:
        camera = Camera.objects.get(id=pk)
        zones = Zone.objects.filter(camera=camera)
        serializer = ZoneSerializer(zones, many=True)
        return Response(serializer.data)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraLinesView(request, pk):
    """Линии для конкретной камеры"""
    try:
        camera = Camera.objects.get(id=pk)
        lines = Line.objects.filter(camera=camera)
        serializer = LineSerializer(lines, many=True)
        return Response(serializer.data)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraRulesView(request, pk):
    """Правила для конкретной камеры"""
    try:
        camera = Camera.objects.get(id=pk)
        rules = Rule.objects.filter(camera=camera)
        serializer = RuleSerializer(rules, many=True)
        return Response(serializer.data)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraEventsView(request, pk):
    """События для конкретной камеры"""
    try:
        camera = Camera.objects.get(id=pk)
        events = Event.objects.filter(camera=camera).order_by('-timestamp')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraVideoFilesView(request, pk):
    """Видео файлы для конкретной камеры"""
    try:
        camera = Camera.objects.get(id=pk)
        video_files = VideoFile.objects.filter(camera=camera).order_by('-start_time')
        serializer = VideoFileSerializer(video_files, many=True)
        return Response(serializer.data)
    except Camera.DoesNotExist:
        return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)


# Rule-specific Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RuleEventsView(request, pk):
    """События для конкретного правила"""
    try:
        rule = Rule.objects.get(id=pk)
        events = Event.objects.filter(rule=rule).order_by('-timestamp')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    except Rule.DoesNotExist:
        return Response({'error': 'Rule not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RuleTestView(request, pk):
    """Тестирование правила"""
    try:
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


# Event-specific Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def EventResolveView(request, pk):
    """Разрешение события"""
    try:
        event = Event.objects.get(id=pk)
        event.resolved = True
        event.resolved_at = timezone.now()
        event.resolved_by = request.user
        event.save()
        
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def EventClipView(request, pk):
    """Клип для события"""
    try:
        event = Event.objects.get(id=pk)
        if event.clip:
            serializer = ClipSerializer(event.clip)
            return Response(serializer.data)
        else:
            return Response({'error': 'No clip available for this event'}, status=status.HTTP_404_NOT_FOUND)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


# Video file-specific Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def VideoFileClipsView(request, pk):
    """Клипы для видео файла"""
    try:
        video_file = VideoFile.objects.get(id=pk)
        clips = Clip.objects.filter(video_file=video_file)
        serializer = ClipSerializer(clips, many=True)
        return Response(serializer.data)
    except VideoFile.DoesNotExist:
        return Response({'error': 'Video file not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def VideoFileDownloadView(request, pk):
    """Скачивание видео файла"""
    try:
        video_file = VideoFile.objects.get(id=pk)
        # Здесь будет реализована логика получения URL для скачивания из MinIO
        result = {
            'video_id': pk,
            'download_url': video_file.storage_path,  # В реальности это будет URL из MinIO
            'file_name': f"{video_file.camera.name}_{video_file.start_time}.mp4",
            'file_size': video_file.file_size
        }
        return Response(result)
    except VideoFile.DoesNotExist:
        return Response({'error': 'Video file not found'}, status=status.HTTP_404_NOT_FOUND)


# Clip-specific Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ClipAnnotationsView(request, pk):
    """Аннотации для клипа"""
    try:
        clip = Clip.objects.get(id=pk)
        annotations = VideoAnnotation.objects.filter(clip=clip)
        serializer = VideoAnnotationSerializer(annotations, many=True)
        return Response(serializer.data)
    except Clip.DoesNotExist:
        return Response({'error': 'Clip not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ClipDownloadView(request, pk):
    """Скачивание клипа"""
    try:
        clip = Clip.objects.get(id=pk)
        result = {
            'clip_id': pk,
            'download_url': clip.download_url,
            'file_name': f"clip_{clip.id}.mp4",
            'start_offset': clip.start_offset,
            'end_offset': clip.end_offset
        }
        return Response(result)
    except Clip.DoesNotExist:
        return Response({'error': 'Clip not found'}, status=status.HTTP_404_NOT_FOUND)


# Health Check
@api_view(['GET'])
def HealthCheckView(request):
    """Проверка состояния сервиса"""
    from django.db import connection
    from django.conf import settings
    
    # Проверяем подключение к базе данных
    try:
        connection.cursor()
        db_status = 'ok'
    except:
        db_status = 'error'
    
    health_status = {
        'status': 'healthy',
        'database': db_status,
        'timestamp': timezone.now(),
        'version': settings.VERSION if hasattr(settings, 'VERSION') else '1.0.0',
        'uptime': 'N/A'  # В реальности здесь будет время работы
    }
    
    return Response(health_status)