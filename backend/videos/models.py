from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.fields import JSONField
from cameras.models import Camera
import uuid


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
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
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