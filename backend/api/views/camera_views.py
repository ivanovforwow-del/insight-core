# views/camera_views.py
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from cameras.models import Camera, Zone, Line
from events.models import Rule
from videos.models import VideoFile, Clip
from events.models import Event

from ..serializers.camera_serializers import (
    CameraSerializer, ZoneSerializer, LineSerializer,
    RuleSerializer, VideoFileSerializer, ClipSerializer
)
from ..services.camera_service import CameraService


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


# Camera-specific Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraZonesView(request, pk):
    """Зоны для конкретной камеры"""
    zones = CameraService.get_camera_zones(pk)
    serializer = ZoneSerializer(zones, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraLinesView(request, pk):
    """Линии для конкретной камеры"""
    lines = CameraService.get_camera_lines(pk)
    serializer = LineSerializer(lines, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraRulesView(request, pk):
    """Правила для конкретной камеры"""
    rules = CameraService.get_camera_rules(pk)
    serializer = RuleSerializer(rules, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraEventsView(request, pk):
    """События для конкретной камеры"""
    events = CameraService.get_camera_events(pk)
    serializer = CameraSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def CameraVideoFilesView(request, pk):
    """Видео файлы для конкретной камеры"""
    video_files = CameraService.get_camera_video_files(pk)
    serializer = VideoFileSerializer(video_files, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def CameraConfigView(request, camera_id):
    """Конфигурация камеры"""
    if request.method == 'GET':
        try:
            camera = Camera.objects.get(id=camera_id)
            serializer = CameraSerializer(camera)
            return Response(serializer.data)
        except Camera.DoesNotExist:
            return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        try:
            config_data = request.data
            updated_camera = CameraService.update_camera_config(camera_id, config_data)
            serializer = CameraSerializer(updated_camera)
            return Response(serializer.data)
        except Camera.DoesNotExist:
            return Response({'error': 'Camera not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)