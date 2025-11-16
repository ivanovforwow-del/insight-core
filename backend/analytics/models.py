from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
import uuid


class MLModel(models.Model):
    """
    Модель машинного обучения для анализа видео
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    model_file = models.FileField(upload_to='ml_models/')
    training_dataset_size = models.PositiveIntegerField(default=0)
    accuracy = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Точность модели от 0 до 1"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=50, default='1.0.0')
    
    class Meta:
        db_table = 'ml_models'
        indexes = [
            models.Index(fields=['name', 'is_active']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} (v{self.version})"


class Camera(models.Model):
    """
    Модель камеры видеонаблюдения
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    rtsp_url = models.URLField(max_length=500)
    location = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('error', 'Error'),
            ('maintenance', 'Maintenance')
        ],
        default='active'
    )
    snapshot = models.ImageField(upload_to='camera_snapshots/', blank=True, null=True)
    vendor = models.CharField(max_length=100, blank=True)
    stream_settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_cameras'
        indexes = [
            models.Index(fields=['status'], name='analytics_cameras_status_idx'),
            models.Index(fields=['created_at'], name='analytics_cameras_created_at_idx'),
        ]
    
    def __str__(self):
        return self.name


class Zone(models.Model):
    """
    Зона интереса на камере (полигон)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='analytics_zones')
    name = models.CharField(max_length=255)
    polygon = models.JSONField(help_text="Координаты полигона в формате [{'x': 0, 'y': 0}, ...]")
    zone_type = models.CharField(
        max_length=50,
        choices=[
            ('entry', 'Entry Zone'),
            ('exit', 'Exit Zone'),
            ('restricted', 'Restricted Area'),
            ('counting', 'Counting Zone'),
            ('detection', 'Detection Zone'),
            ('custom', 'Custom Zone')
        ]
    )
    allowed_objects = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Разрешенные типы объектов (person, car, truck, etc.)"
    )
    forbidden_objects = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Запрещенные типы объектов"
    )
    max_objects = models.PositiveIntegerField(default=0, help_text="Максимальное количество объектов в зоне (0 = без ограничений)")
    min_duration = models.PositiveIntegerField(default=0, help_text="Минимальная продолжительность пребывания в зоне (секунды)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_zones'
        indexes = [
            models.Index(fields=['camera', 'zone_type'], name='analytics_zones_camera_zone_type_idx'),
            models.Index(fields=['is_active'], name='analytics_zones_is_active_idx'),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"


class Line(models.Model):
    """
    Линия интереса на камере (для подсчета пересечений)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='analytics_lines')
    name = models.CharField(max_length=255)
    points = models.JSONField(help_text="Координаты линии в формате [{'x': 0, 'y': 0}, {'x': 1, 'y': 1}]")
    direction = models.CharField(
        max_length=20,
        choices=[
            ('horizontal', 'Horizontal'),
            ('vertical', 'Vertical'),
            ('custom', 'Custom')
        ],
        default='custom'
    )
    allowed_objects = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )
    forbidden_objects = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_lines'
        indexes = [
            models.Index(fields=['camera', 'direction'], name='analytics_lines_camera_direction_idx'),
            models.Index(fields=['is_active'], name='analytics_lines_is_active_idx'),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"


class Rule(models.Model):
    """
    Правило аналитики (условия срабатывания)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='analytics_rules')
    rule_type = models.CharField(
        max_length=50,
        choices=[
            ('line_crossing', 'Line Crossing'),
            ('zone_violation', 'Zone Violation'),
            ('behavior_detection', 'Behavior Detection'),
            ('loitering', 'Loitering'),
            ('object_left_behind', 'Object Left Behind'),
            ('speed_detection', 'Speed Detection'),
            ('counting', 'Counting'),
            ('custom', 'Custom Rule')
        ]
    )
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name='analytics_rules')
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True, blank=True, related_name='analytics_rules')
    conditions = models.JSONField(default=dict, help_text="Условия срабатывания правила")
    severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical')
        ],
        default='medium'
    )
    enabled = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_rules'
        indexes = [
            models.Index(fields=['camera', 'rule_type'], name='analytics_rules_camera_rule_type_idx'),
            models.Index(fields=['severity', 'enabled'], name='analytics_rules_severity_enabled_idx'),
            models.Index(fields=['created_at'], name='analytics_rules_created_at_idx'),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"


class VideoFile(models.Model):
    """
    Файл видео с камеры
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='analytics_video_files')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField(help_text="Длительность в секундах")
    storage_path = models.CharField(max_length=500, help_text="Путь к файлу в MinIO")
    file_size = models.BigIntegerField(help_text="Размер файла в байтах")
    fps = models.FloatField(help_text="Кадры в секунду")
    resolution = models.CharField(max_length=20, help_text="Разрешение (например, 1920x1080)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_video_files'
        indexes = [
            models.Index(fields=['camera', 'start_time'], name='analytics_video_files_camera_start_time_idx'),
            models.Index(fields=['created_at'], name='analytics_video_files_created_at_idx'),
        ]
    
    def __str__(self):
        return f"{self.camera.name} - {self.start_time}"


class Clip(models.Model):
    """
    Клип/фрагмент видео с событием
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_file = models.ForeignKey(VideoFile, on_delete=models.CASCADE, related_name='analytics_clips')
    start_offset = models.FloatField(help_text="Начало клипа в секундах от начала видео")
    end_offset = models.FloatField(help_text="Конец клипа в секундах от начала видео")
    label = models.CharField(max_length=255, blank=True)
    download_url = models.URLField(max_length=500, blank=True)
    is_annotated = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='clip_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_clips'
        indexes = [
            models.Index(fields=['video_file', 'start_offset'], name='analytics_clips_video_file_start_offset_idx'),
            models.Index(fields=['is_annotated'], name='analytics_clips_is_annotated_idx'),
            models.Index(fields=['created_at'], name='analytics_clips_created_at_idx'),
        ]
    
    def __str__(self):
        return f"Clip {self.start_offset}-{self.end_offset}s from {self.video_file}"


class VideoAnnotation(models.Model):
    """
    Аннотация к видео (для обучения моделей)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE, related_name='analytics_annotations')
    label = models.CharField(max_length=255)
    start_time = models.FloatField(help_text="Время начала в секундах от начала клипа")
    end_time = models.FloatField(help_text="Время окончания в секундах от начала клипа")
    bbox = models.JSONField(help_text="Координаты bounding box в формате {'x': 0, 'y': 0, 'w': 0, 'h': 0}")
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics_video_annotations_created_by_user')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_video_annotations'
        indexes = [
            models.Index(fields=['clip', 'label'], name='analytics_video_annot_clip_label_idx'),
            models.Index(fields=['status'], name='analytics_video_annot_status_idx'),
            models.Index(fields=['created_at'], name='analytics_video_annot_created_at_idx'),
        ]
    
    def __str__(self):
        return f"{self.label} annotation for {self.clip}"


class Event(models.Model):
    """
    Событие, зафиксированное аналитикой
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rule = models.ForeignKey('events.Rule', on_delete=models.CASCADE, related_name='analytics_events')
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='analytics_events')
    timestamp = models.DateTimeField()
    object_class = models.CharField(max_length=100, help_text="Класс обнаруженного объекта")
    track_id = models.CharField(max_length=100, help_text="ID трека объекта")
    bbox = models.JSONField(help_text="Координаты bounding box")
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    severity = models.CharField(max_length=20, choices=Rule.severity.field.choices)
    clip = models.ForeignKey(Clip, on_delete=models.SET_NULL, null=True, blank=True, related_name='analytics_events')
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='analytics_events_resolved_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'analytics_events'
        indexes = [
            models.Index(fields=['camera', 'timestamp'], name='analytics_events_camera_timestamp_idx'),
            models.Index(fields=['rule', 'severity'], name='analytics_events_rule_severity_idx'),
            models.Index(fields=['resolved', 'timestamp'], name='analytics_events_resolved_timestamp_idx'),
            GinIndex(fields=['bbox'], name='analytics_events_bbox_gin'),  # Для поиска по JSON
        ]
    
    def __str__(self):
        return f"{self.object_class} event at {self.timestamp}"

