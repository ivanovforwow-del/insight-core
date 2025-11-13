from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.fields import JSONField
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
    stream_settings = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cameras'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return self.name


class Zone(models.Model):
    """
    Зона интереса на камере (полигон)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='zones')
    name = models.CharField(max_length=255)
    polygon = JSONField(help_text="Координаты полигона в формате [{'x': 0, 'y': 0}, ...]")
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
        db_table = 'zones'
        indexes = [
            models.Index(fields=['camera', 'zone_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"


class Line(models.Model):
    """
    Линия интереса на камере (для подсчета пересечений)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='lines')
    name = models.CharField(max_length=255)
    points = JSONField(help_text="Координаты линии в формате [{'x': 0, 'y': 0}, {'x': 1, 'y': 1}]")
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
        db_table = 'lines'
        indexes = [
            models.Index(fields=['camera', 'direction']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"


class Rule(models.Model):
    """
    Правило аналитики (условия срабатывания)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='rules')
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
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name='rules')
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True, blank=True, related_name='rules')
    conditions = JSONField(default=dict, help_text="Условия срабатывания правила")
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
        db_table = 'rules'
        indexes = [
            models.Index(fields=['camera', 'rule_type']),
            models.Index(fields=['severity', 'enabled']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"


class VideoFile(models.Model):
    """
    Файл видео с камеры
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='video_files')
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
        db_table = 'video_files'
        indexes = [
            models.Index(fields=['camera', 'start_time']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.camera.name} - {self.start_time}"


class Clip(models.Model):
    """
    Клип/фрагмент видео с событием
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_file = models.ForeignKey(VideoFile, on_delete=models.CASCADE, related_name='clips')
    start_offset = models.FloatField(help_text="Начало клипа в секундах от начала видео")
    end_offset = models.FloatField(help_text="Конец клипа в секундах от начала видео")
    label = models.CharField(max_length=255, blank=True)
    download_url = models.URLField(max_length=500, blank=True)
    is_annotated = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='clip_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clips'
        indexes = [
            models.Index(fields=['video_file', 'start_offset']),
            models.Index(fields=['is_annotated']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Clip {self.start_offset}-{self.end_offset}s from {self.video_file}"


class VideoAnnotation(models.Model):
    """
    Аннотация к видео (для обучения моделей)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE, related_name='annotations')
    label = models.CharField(max_length=255)
    start_time = models.FloatField(help_text="Время начала в секундах от начала клипа")
    end_time = models.FloatField(help_text="Время окончания в секундах от начала клипа")
    bbox = JSONField(help_text="Координаты bounding box в формате {'x': 0, 'y': 0, 'w': 0, 'h': 0}")
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
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
        db_table = 'video_annotations'
        indexes = [
            models.Index(fields=['clip', 'label']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.label} annotation for {self.clip}"


class Event(models.Model):
    """
    Событие, зафиксированное аналитикой
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='events')
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='events')
    timestamp = models.DateTimeField()
    object_class = models.CharField(max_length=100, help_text="Класс обнаруженного объекта")
    track_id = models.CharField(max_length=100, help_text="ID трека объекта")
    bbox = JSONField(help_text="Координаты bounding box")
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    severity = models.CharField(max_length=20, choices=Rule.severity.field.choices)
    clip = models.ForeignKey(Clip, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'events'
        indexes = [
            models.Index(fields=['camera', 'timestamp']),
            models.Index(fields=['rule', 'severity']),
            models.Index(fields=['resolved', 'timestamp']),
            GinIndex(fields=['bbox']),  # Для поиска по JSON
        ]
    
    def __str__(self):
        return f"{self.object_class} event at {self.timestamp}"


class AlertChannel(models.Model):
    """
    Канал оповещений
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    channel_type = models.CharField(
        max_length=50,
        choices=[
            ('telegram', 'Telegram'),
            ('email', 'Email'),
            ('webhook', 'Webhook'),
            ('sms', 'SMS'),
            ('push', 'Push Notification')
        ]
    )
    config = JSONField(help_text="Конфигурация канала (токены, адреса и т.д.)")
    enabled = models.BooleanField(default=True)
    schedule = JSONField(default=dict, blank=True, help_text="Расписание отправки уведомлений")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'alert_channels'
        indexes = [
            models.Index(fields=['channel_type', 'enabled']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.channel_type})"


class Alert(models.Model):
    """
    Оповещение, отправленное по событию
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='alerts')
    channel = models.ForeignKey(AlertChannel, on_delete=models.CASCADE, related_name='alerts')
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('failed', 'Failed'),
            ('delivered', 'Delivered')
        ],
        default='pending'
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    message = models.TextField()
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'alerts'
        indexes = [
            models.Index(fields=['event', 'status']),
            models.Index(fields=['channel', 'status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Alert for {self.event} via {self.channel}"