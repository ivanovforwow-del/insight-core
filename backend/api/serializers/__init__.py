# Import all serializers to make them available when importing from api.serializers
from .alert_serializers import *
from .analytics_serializers import *
from .camera_serializers import *
from .event_serializers import *
from .video_serializers import *

# Also import UserSerializer which is in the main serializers.py file
from ..serializers import UserSerializer