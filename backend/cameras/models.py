from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
import uuid


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
        db_table = 'cameras_cameras'
        indexes = [
            models.Index(fields=['status'], name='cameras_cameras_status_idx'),
            models.Index(fields=['created_at'], name='cameras_cameras_created_at_idx'),
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
        db_table = 'cameras_zones'
        indexes = [
            models.Index(fields=['camera', 'zone_type'], name='cameras_zones_camera_zone_type_idx'),
            models.Index(fields=['is_active'], name='cameras_zones_is_active_idx'),
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
        db_table = 'cameras_lines'
        indexes = [
            models.Index(fields=['camera', 'direction'], name='cameras_lines_camera_direction_idx'),
            models.Index(fields=['is_active'], name='cameras_lines_is_active_idx'),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"