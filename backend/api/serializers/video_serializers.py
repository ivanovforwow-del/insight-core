# serializers/video_serializers.py
from rest_framework import serializers
from videos.models import VideoFile, Clip, VideoAnnotation


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