# Import all views from the different view modules to make them available in the main views module
from .alert_views import *
from .analytics_views import *
from .camera_views import *
from .dashboard_views import *
from .event_views import *
from .video_views import *
from .common_views import *

# Also import any viewsets or other classes that might be defined directly in this package
# This ensures that all views are available when using 'from api.views import *' or 'from . import views'