from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()

# Analytics endpoints
# router.register(r'ml-models', views.MLModelViewSet, basename='mlmodel')
# router.register(r'cameras', views.CameraViewSet, basename='camera')
# router.register(r'zones', views.ZoneViewSet, basename='zone')
# router.register(r'lines', views.LineViewSet, basename='line')
# router.register(r'rules', views.RuleViewSet, basename='rule')

# Video-related endpoints
# router.register(r'video-files', views.VideoFileViewSet, basename='videofile')
# router.register(r'clips', views.ClipViewSet, basename='clip')
# router.register(r'video-annotations', views.VideoAnnotationViewSet, basename='videoannotation')

# Events and alerts
# router.register(r'events', views.EventViewSet, basename='event')
# router.register(r'alert-channels', views.AlertChannelViewSet, basename='alertchannel')
# router.register(r'alerts', views.AlertViewSet, basename='alert')

# Define URL patterns
urlpatterns = [
    # API root
    path('', include(router.urls)),
    
    # Authentication endpoints
    # path('auth/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/token/verify/', views.CustomTokenVerifyView.as_view(), name='token_verify'),
    
    # Dashboard endpoints
    path('dashboard/stats/', views.DashboardStatsView, name='dashboard-stats'),
    # path('dashboard/events/', views.DashboardEventsView.as_view(), name='dashboard-events'),
    # path('dashboard/cameras/', views.DashboardCamerasView.as_view(), name='dashboard-cameras'),
    
    # Video processing endpoints
    path('video/analyze/', views.VideoAnalysisView, name='video-analyze'),
    # path('video/process/', views.VideoProcessView.as_view(), name='video-process'),
    # path('video/upload/', views.VideoUploadView.as_view(), name='video-upload'),
    
    # Live stream endpoints
    # path('stream/<uuid:camera_id>/', views.LiveStreamView.as_view(), name='live-stream'),
    # path('stream/<uuid:camera_id>/snapshot/', views.SnapshotView.as_view(), name='snapshot'),
    
    # Analytics endpoints
    # path('analytics/heatmap/', views.HeatmapView.as_view(), name='heatmap'),
    # path('analytics/timeline/', views.TimelineView.as_view(), name='timeline'),
    # path('analytics/report/', views.AnalyticsReportView.as_view(), name='analytics-report'),
    
    # Alert management
    # path('alerts/send/', views.SendAlertView.as_view(), name='send-alert'),
    # path('alerts/batch/', views.BatchAlertView.as_view(), name='batch-alert'),
    
    # Configuration endpoints
    # path('config/camera/<uuid:camera_id>/', views.CameraConfigView.as_view(), name='camera-config'),
    # path('config/rules/', views.RulesConfigView.as_view(), name='rules-config'),
    
    # Health check
    path('health/', views.HealthCheckView, name='health-check'),
]

# Additional URL patterns for specific use cases
urlpatterns += [
    # Camera-specific endpoints
    path('cameras/<uuid:pk>/zones/', views.CameraZonesView, name='camera-zones'),
    path('cameras/<uuid:pk>/lines/', views.CameraLinesView, name='camera-lines'),
    path('cameras/<uuid:pk>/rules/', views.CameraRulesView, name='camera-rules'),
    path('cameras/<uuid:pk>/events/', views.CameraEventsView, name='camera-events'),
    path('cameras/<uuid:pk>/video-files/', views.CameraVideoFilesView, name='camera-video-files'),
    
    # Rule-specific endpoints
    path('rules/<uuid:pk>/events/', views.RuleEventsView, name='rule-events'),
    path('rules/<uuid:pk>/test/', views.RuleTestView, name='rule-test'),
    
    # Event-specific endpoints
    path('events/<uuid:pk>/resolve/', views.EventResolveView, name='event-resolve'),
    path('events/<uuid:pk>/clip/', views.EventClipView, name='event-clip'),
    
    # Video file-specific endpoints
    path('video-files/<uuid:pk>/clips/', views.VideoFileClipsView, name='videofile-clips'),
    path('video-files/<uuid:pk>/download/', views.VideoFileDownloadView, name='videofile-download'),
    
    # Clip-specific endpoints
    path('clips/<uuid:pk>/annotations/', views.ClipAnnotationsView, name='clip-annotations'),
    path('clips/<uuid:pk>/download/', views.ClipDownloadView, name='clip-download'),
]