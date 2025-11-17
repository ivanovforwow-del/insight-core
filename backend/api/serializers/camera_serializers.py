# serializers/camera_serializers.py
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User
from cameras.models import Camera, Zone, Line
from events.models import Rule
from videos.models import VideoFile, Clip, VideoAnnotation


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'name': _('Название'),
            'rtsp_url': _('RTSP URL'),
            'location': _('Местоположение'),
            'status': _('Статус'),
            'snapshot': _('Снимок'),
            'vendor': _('Производитель'),
            'stream_settings': _('Настройки потока'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'name': _('Название'),
            'camera': _('Камера'),
            'polygon': _('Полигон'),
            'zone_type': _('Тип зоны'),
            'allowed_objects': _('Разрешенные объекты'),
            'forbidden_objects': _('Запрещенные объекты'),
            'max_objects': _('Максимальное количество объектов'),
            'min_duration': _('Минимальная продолжительность'),
            'is_active': _('Активна'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }


class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'name': _('Название'),
            'camera': _('Камера'),
            'points': _('Координаты'),
            'direction': _('Направление'),
            'allowed_objects': _('Разрешенные объекты'),
            'forbidden_objects': _('Запрещенные объекты'),
            'is_active': _('Активна'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'name': _('Название'),
            'camera': _('Камера'),
            'rule_type': _('Тип правила'),
            'zone': _('Зона'),
            'line': _('Линия'),
            'conditions': _('Условия'),
            'severity': _('Уровень серьезности'),
            'enabled': _('Активно'),
            'description': _('Описание'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }


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