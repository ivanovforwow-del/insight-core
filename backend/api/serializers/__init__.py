# Import all serializers to make them available when importing from api.serializers
from .alert_serializers import *
from .analytics_serializers import *
from .camera_serializers import *
from .event_serializers import *
from .video_serializers import *

# UserSerializer is available from the main serializers.py file
# Import it directly from api.serializers when needed