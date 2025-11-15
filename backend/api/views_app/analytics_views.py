# views/analytics_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..services.analytics_service import AnalyticsService


# Analytics Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def HeatmapView(request):
    """Тепловая карта событий"""
    camera_id = request.query_params.get('camera_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    result = AnalyticsService.get_heatmap_data(
        camera_id=int(camera_id) if camera_id else None,
        start_date=start_date,
        end_date=end_date
    )
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def TimelineView(request):
    """Временная шкала событий"""
    camera_id = request.query_params.get('camera_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    result = AnalyticsService.get_timeline_data(
        camera_id=int(camera_id) if camera_id else None,
        start_date=start_date,
        end_date=end_date
    )
    return Response(result)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def AnalyticsReportView(request):
    """Отчет по аналитике"""
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    result = AnalyticsService.get_analytics_report(
        start_date=start_date,
        end_date=end_date
    )
    return Response(result)