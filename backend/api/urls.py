from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it
router = DefaultRouter()

# Analytics endpoints
# Используем прямой импорт из модуля views.py, а не из пакета views/
from .views import (
    MLModelViewSet, CameraViewSet, ZoneViewSet, LineViewSet,
    RuleViewSet, VideoFileViewSet, ClipViewSet, VideoAnnotationViewSet,
    EventViewSet, AlertChannelViewSet, AlertViewSet,
    # Authentication views
    CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView,
    # Dashboard views
    DashboardStatsView, DashboardEventsView, DashboardCamerasView,
    # Video processing views
    VideoAnalysisView, VideoProcessView, VideoUploadView,
    # Live stream views
    LiveStreamView, SnapshotView,
    # Analytics views
    HeatmapView, TimelineView, AnalyticsReportView,
    # Alert management views
    SendAlertView, BatchAlertView,
    # Configuration views
    CameraConfigView, RulesConfigView,
    # Health check view
    HealthCheckView,
    # Camera-specific views
    CameraZonesView, CameraLinesView, CameraRulesView, CameraEventsView, CameraVideoFilesView,
    # Rule-specific views
    RuleEventsView, RuleTestView,
    # Event-specific views
    EventResolveView, EventClipView,
    # Video file-specific views
    VideoFileClipsView, VideoFileDownloadView,
    # Clip-specific views
    ClipAnnotationsView, ClipDownloadView
)

def get_camera_viewset():
    return CameraViewSet

def get_zone_viewset():
    return ZoneViewSet

def get_line_viewset():
    return LineViewSet

def get_rule_viewset():
    return RuleViewSet

def get_video_file_viewset():
    return VideoFileViewSet

def get_clip_viewset():
    return ClipViewSet

def get_video_annotation_viewset():
    return VideoAnnotationViewSet

def get_event_viewset():
    return EventViewSet

def get_alert_channel_viewset():
    return AlertChannelViewSet

def get_alert_viewset():
    return AlertViewSet

router.register(r'ml-models', MLModelViewSet, basename='mlmodel')
router.register(r'cameras', get_camera_viewset(), basename='camera')
router.register(r'zones', get_zone_viewset(), basename='zone')
router.register(r'lines', get_line_viewset(), basename='line')
router.register(r'rules', get_rule_viewset(), basename='rule')

# Video-related endpoints
router.register(r'video-files', get_video_file_viewset(), basename='videofile')
router.register(r'clips', get_clip_viewset(), basename='clip')
router.register(r'video-annotations', get_video_annotation_viewset(), basename='videoannotation')

# Events and alerts
router.register(r'events', get_event_viewset(), basename='event')
router.register(r'alert-channels', get_alert_channel_viewset(), basename='alertchannel')
router.register(r'alerts', get_alert_viewset(), basename='alert')

# Define URL patterns
urlpatterns = [
    # API root
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    
    # Dashboard endpoints
    path('dashboard/stats/', DashboardStatsView, name='dashboard-stats'),
    path('dashboard/events/', DashboardEventsView, name='dashboard-events'),
    path('dashboard/cameras/', DashboardCamerasView, name='dashboard-cameras'),
    
    # Video processing endpoints
    path('video/analyze/', VideoAnalysisView, name='video-analyze'),
    path('video/process/', VideoProcessView, name='video-process'),
    path('video/upload/', VideoUploadView, name='video-upload'),
    
    # Live stream endpoints
    path('stream/<uuid:camera_id>/', LiveStreamView, name='live-stream'),
    path('stream/<uuid:camera_id>/snapshot/', SnapshotView, name='snapshot'),
    
    # Analytics endpoints
    path('analytics/heatmap/', HeatmapView, name='heatmap'),
    path('analytics/timeline/', TimelineView, name='timeline'),
    path('analytics/report/', AnalyticsReportView, name='analytics-report'),
    
    # Alert management
    path('alerts/send/', SendAlertView, name='send-alert'),
    path('alerts/batch/', BatchAlertView, name='batch-alert'),
    
    # Configuration endpoints
    path('config/camera/<uuid:camera_id>/', CameraConfigView, name='camera-config'),
    path('config/rules/', RulesConfigView, name='rules-config'),
    
    # Health check
    path('health/', HealthCheckView, name='health-check'),
]

# Additional URL patterns for specific use cases
urlpatterns += [
    # Camera-specific endpoints
    path('cameras/<uuid:pk>/zones/', CameraZonesView, name='camera-zones'),
    path('cameras/<uuid:pk>/lines/', CameraLinesView, name='camera-lines'),
    path('cameras/<uuid:pk>/rules/', CameraRulesView, name='camera-rules'),
    path('cameras/<uuid:pk>/events/', CameraEventsView, name='camera-events'),
    path('cameras/<uuid:pk>/video-files/', CameraVideoFilesView, name='camera-video-files'),
    
    # Rule-specific endpoints
    path('rules/<uuid:pk>/events/', RuleEventsView, name='rule-events'),
    path('rules/<uuid:pk>/test/', RuleTestView, name='rule-test'),
    
    # Event-specific endpoints
    path('events/<uuid:pk>/resolve/', EventResolveView, name='event-resolve'),
    path('events/<uuid:pk>/clip/', EventClipView, name='event-clip'),
    
    # Video file-specific endpoints
    path('video-files/<uuid:pk>/clips/', VideoFileClipsView, name='videofile-clips'),
    path('video-files/<uuid:pk>/download/', VideoFileDownloadView, name='videofile-download'),
    
    # Clip-specific endpoints
    path('clips/<uuid:pk>/annotations/', ClipAnnotationsView, name='clip-annotations'),
    path('clips/<uuid:pk>/download/', ClipDownloadView, name='clip-download'),
]