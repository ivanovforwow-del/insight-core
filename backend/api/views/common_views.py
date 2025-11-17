# Common views that don't fit into specific categories
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


class CustomTokenObtainPairView(TokenObtainPairView):
    pass


class CustomTokenRefreshView(TokenRefreshView):
    pass


class CustomTokenVerifyView(TokenVerifyView):
    pass


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.conf import settings
from django.utils import timezone


from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.conf import settings
import json


@csrf_exempt
def HealthCheckView(request):
    """Проверка состояния сервиса"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    # Проверяем подключение к базе данных, обходя кеш
    try:
        connection = connections['default']
        connection.ensure_connection()
        db_status = 'ok'
    except OperationalError:
        db_status = 'error'
    
    health_status = {
        'status': 'healthy' if db_status == 'ok' else 'unhealthy',
        'database': db_status,
        'timestamp': timezone.now().isoformat(),
        'version': getattr(settings, 'VERSION', '1.0.0'),
        'uptime': 'N/A'  # В реальности здесь будет время работы
    }
    
    return JsonResponse(health_status)