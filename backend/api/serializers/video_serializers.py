# serializers/video_serializers.py
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from videos.models import VideoFile, Clip, VideoAnnotation


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'camera': _('Камера'),
            'start_time': _('Время начала'),
            'end_time': _('Время окончания'),
            'duration': _('Длительность'),
            'storage_path': _('Путь к файлу'),
            'file_size': _('Размер файла'),
            'fps': _('Кадры в секунду'),
            'resolution': _('Разрешение'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }


class ClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clip
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'video_file': _('Видео файл'),
            'start_offset': _('Начало клипа'),
            'end_offset': _('Конец клипа'),
            'label': _('Метка'),
            'download_url': _('URL для скачивания'),
            'is_annotated': _('Аннотирован'),
            'thumbnail': _('Миниатюра'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }


class VideoAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoAnnotation
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'clip': _('Клип'),
            'label': _('Метка'),
            'start_time': _('Время начала'),
            'end_time': _('Время окончания'),
            'bbox': _('Границы объекта'),
            'confidence': _('Уверенность'),
            'created_by': _('Создано пользователем'),
            'status': _('Статус'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }