# serializers/camera_serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from cameras.models import Camera, Zone, Line
from events.models import Rule
from videos.models import VideoFile, Clip, VideoAnnotation


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