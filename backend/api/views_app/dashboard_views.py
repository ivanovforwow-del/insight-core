# views/dashboard_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..services.dashboard_service import DashboardService


# Dashboard Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def DashboardStatsView(request):
    """Статистика для дашборда"""
    stats = DashboardService.get_dashboard_stats()
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def DashboardEventsView(request):
    """События для дашборда"""
    events_data = DashboardService.get_dashboard_events()
    return Response(events_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def DashboardCamerasView(request):
    """Камеры для дашборда"""
    cameras_data = DashboardService.get_dashboard_cameras()
    return Response(cameras_data)