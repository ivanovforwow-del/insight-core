from rest_framework import serializers
from django.contrib.auth.models import User
from cameras.models import Camera, Zone, Line
from videos.models import VideoFile, Clip, VideoAnnotation
from events.models import Rule, Event
from alerts.models import AlertChannel, Alert
from analytics.models import MLModel


class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = '__all__'


class ClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clip
        fields = '__all__'


class VideoAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoAnnotation
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class AlertChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertChannel
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']