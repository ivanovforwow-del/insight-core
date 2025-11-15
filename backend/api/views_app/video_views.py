# views/video_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta

from videos.models import VideoFile, Clip, VideoAnnotation
from ..serializers.video_serializers import (
    VideoFileSerializer, ClipSerializer, VideoAnnotationSerializer
)
from ..services.video_service import VideoService


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


# Video Processing Views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def VideoAnalysisView(request):
    """Анализ видео файла"""
    video_id = request.data.get('video_id')
    if not video_id:
        return Response({'error': 'Video ID is required'}, status=400)
    
    try:
        result = VideoService.create_video_analysis_job(video_id)
        return Response(result)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def VideoProcessView(request):
    """Обработка видео файла"""
    video_file = request.FILES.get('video')
    if not video_file:
        return Response({'error': 'Video file is required'}, status=400)
    
    # This would need to be integrated with actual video processing
    # For now, returning a placeholder response
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
        return Response({'error': 'Video file and camera ID are required'}, status=400)
    
    try:
        result = VideoService.upload_video_file(video_file, camera_id)
        return Response(result)
    except ValueError as e:
        return Response({'error': str(e)}, status=404)


# Live Stream Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def LiveStreamView(request, camera_id):
    """Потоковое видео с камеры"""
    try:
        result = VideoService.get_live_stream_url(camera_id)
        return Response(result)
    except ValueError as e:
        return Response({'error': str(e)}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def SnapshotView(request, camera_id):
    """Снимок с камеры"""
    try:
        result = VideoService.get_camera_snapshot(camera_id)
        return Response(result)
    except ValueError as e:
        return Response({'error': str(e)}, status=404)


# Video file-specific Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def VideoFileClipsView(request, pk):
    """Клипы для видео файла"""
    try:
        clips = VideoService.get_video_clips(pk)
        from ..serializers.video_serializers import ClipSerializer
        serializer = ClipSerializer(clips, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def VideoFileDownloadView(request, pk):
    """Скачивание видео файла"""
    try:
        result = VideoService.get_video_file_download_info(pk)
        return Response(result)
    except ValueError as e:
        return Response({'error': str(e)}, status=404)


# Clip-specific Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ClipAnnotationsView(request, pk):
    """Аннотации для клипа"""
    try:
        annotations = VideoService.get_clip_annotations(pk)
        serializer = VideoAnnotationSerializer(annotations, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ClipDownloadView(request, pk):
    """Скачивание клипа"""
    try:
        result = VideoService.get_clip_download_info(pk)
        return Response(result)
    except ValueError as e:
        return Response({'error': str(e)}, status=404)