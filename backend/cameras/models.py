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
    verbose_name = "Камера"
    verbose_name_plural = "Камеры"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название")
    rtsp_url = models.URLField(max_length=500)
    location = models.CharField(max_length=500, blank=True, verbose_name="Местоположение")
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Активна'),
            ('inactive', 'Неактивна'),
            ('error', 'Ошибка'),
            ('maintenance', 'Обслуживание')
        ],
        default='active',
        verbose_name="Статус"
    )
    snapshot = models.ImageField(upload_to='camera_snapshots/', blank=True, null=True, verbose_name="Снимок")
    vendor = models.CharField(max_length=100, blank=True, verbose_name="Производитель")
    stream_settings = models.JSONField(default=dict, blank=True, verbose_name="Настройки потока")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'cameras_cameras'
        verbose_name = "Камера"
        verbose_name_plural = "Камеры"
        indexes = [
            models.Index(fields=['status'], name='cameras_cameras_status_idx'),
            models.Index(fields=['created_at'], name='cameras_cameras_created_at_idx'),
        ]
    
    def __str__(self):
        return self.name
    
    def get_status_display(self):
        STATUS_CHOICES = [
            ('active', 'Активна'),
            ('inactive', 'Неактивна'),
            ('error', 'Ошибка'),
            ('maintenance', 'Обслуживание')
        ]
        for choice_key, choice_value in STATUS_CHOICES:
            if choice_key == self.status:
                return choice_value
        return self.status


class Zone(models.Model):
    """
    Зона интереса на камере (полигон)
    """
    verbose_name = "Зона"
    verbose_name_plural = "Зоны"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='zones', verbose_name="Камера")
    name = models.CharField(max_length=255, verbose_name="Название")
    polygon = models.JSONField(help_text="Координаты полигона в формате [{'x': 0, 'y': 0}, ...]", verbose_name="Полигон")
    zone_type = models.CharField(
        max_length=50,
        choices=[
            ('entry', 'Зона входа'),
            ('exit', 'Зона выхода'),
            ('restricted', 'Запретная зона'),
            ('counting', 'Зона подсчета'),
            ('detection', 'Зона обнаружения'),
            ('custom', 'Пользовательская зона')
        ],
        verbose_name="Тип зоны"
    )
    allowed_objects = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Разрешенные типы объектов (person, car, truck, etc.)",
        verbose_name="Разрешенные объекты"
    )
    forbidden_objects = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        help_text="Запрещенные типы объектов",
        verbose_name="Запрещенные объекты"
    )
    max_objects = models.PositiveIntegerField(default=0, help_text="Максимальное количество объектов в зоне (0 = без ограничений)", verbose_name="Максимальное количество объектов")
    min_duration = models.PositiveIntegerField(default=0, help_text="Минимальная продолжительность пребывания в зоне (секунды)", verbose_name="Минимальная продолжительность")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'cameras_zones'
        verbose_name = "Зона"
        verbose_name_plural = "Зоны"
        indexes = [
            models.Index(fields=['camera', 'zone_type'], name='cam_zones_cam_zone_type_idx'),
            models.Index(fields=['is_active'], name='cameras_zones_is_active_idx'),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"
    
    def get_zone_type_display(self):
        ZONE_TYPE_CHOICES = [
            ('entry', 'Зона входа'),
            ('exit', 'Зона выхода'),
            ('restricted', 'Запретная зона'),
            ('counting', 'Зона подсчета'),
            ('detection', 'Зона обнаружения'),
            ('custom', 'Пользовательская зона')
        ]
        for choice_key, choice_value in ZONE_TYPE_CHOICES:
            if choice_key == self.zone_type:
                return choice_value
        return self.zone_type


class Line(models.Model):
    """
    Линия интереса на камере (для подсчета пересечений)
    """
    verbose_name = "Линия"
    verbose_name_plural = "Линии"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='lines', verbose_name="Камера")
    name = models.CharField(max_length=255, verbose_name="Название")
    points = models.JSONField(help_text="Координаты линии в формате [{'x': 0, 'y': 0}, {'x': 1, 'y': 1}]", verbose_name="Координаты")
    direction = models.CharField(
        max_length=20,
        choices=[
            ('horizontal', 'Горизонтальная'),
            ('vertical', 'Вертикальная'),
            ('custom', 'Пользовательская')
        ],
        default='custom',
        verbose_name="Направление"
    )
    allowed_objects = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        verbose_name="Разрешенные объекты"
    )
    forbidden_objects = ArrayField(
        models.CharField(max_length=50),
        default=list,
        blank=True,
        verbose_name="Запрещенные объекты"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'cameras_lines'
        verbose_name = "Линия"
        verbose_name_plural = "Линии"
        indexes = [
            models.Index(fields=['camera', 'direction'], name='cam_lines_cam_direction_idx'),
            models.Index(fields=['is_active'], name='cameras_lines_is_active_idx'),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"
    
    def get_direction_display(self):
        DIRECTION_CHOICES = [
            ('horizontal', 'Горизонтальная'),
            ('vertical', 'Вертикальная'),
            ('custom', 'Пользовательская')
        ]
        for choice_key, choice_value in DIRECTION_CHOICES:
            if choice_key == self.direction:
                return choice_value
        return self.direction