# Common views that don't fit into specific categories
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from django.conf import settings
from django.utils import timezone


@api_view(['GET'])
def HealthCheckView(request):
    """Проверка состояния сервиса"""
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
        'version': getattr(settings, 'VERSION', '1.0.0'),
        'uptime': 'N/A'  # В реальности здесь будет время работы
    }
    
    return Response(health_status)