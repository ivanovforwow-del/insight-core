from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from cameras.models import Camera
import uuid


class VideoFile(models.Model):
    """
    Файл видео с камеры
    """
    verbose_name = "Видео файл"
    verbose_name_plural = "Видео файлы"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='video_files', verbose_name="Камера")
    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время окончания")
    duration = models.FloatField(help_text="Длительность в секундах", verbose_name="Длительность")
    storage_path = models.CharField(max_length=500, help_text="Путь к файлу в MinIO", verbose_name="Путь к файлу")
    file_size = models.BigIntegerField(help_text="Размер файла в байтах", verbose_name="Размер файла")
    fps = models.FloatField(help_text="Кадры в секунду", verbose_name="Кадры в секунду")
    resolution = models.CharField(max_length=20, help_text="Разрешение (например, 1920x1080)", verbose_name="Разрешение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'videos_video_files'
        verbose_name = "Видео файл"
        verbose_name_plural = "Видео файлы"
        indexes = [
            models.Index(fields=['camera', 'start_time'], name='vid_files_cam_start_time_idx'),
            models.Index(fields=['created_at'], name='vid_files_created_at_idx'),
        ]
    
    def __str__(self):
        return f"{self.camera.name} - {self.start_time}"


class Clip(models.Model):
    """
    Клип/фрагмент видео с событием
    """
    verbose_name = "Клип"
    verbose_name_plural = "Клипы"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_file = models.ForeignKey(VideoFile, on_delete=models.CASCADE, related_name='clips', verbose_name="Видео файл")
    start_offset = models.FloatField(help_text="Начало клипа в секундах от начала видео", verbose_name="Начало клипа")
    end_offset = models.FloatField(help_text="Конец клипа в секундах от начала видео", verbose_name="Конец клипа")
    label = models.CharField(max_length=255, blank=True, verbose_name="Метка")
    download_url = models.URLField(max_length=500, blank=True, verbose_name="URL для скачивания")
    is_annotated = models.BooleanField(default=False, verbose_name="Аннотирован")
    thumbnail = models.ImageField(upload_to='clip_thumbnails/', blank=True, null=True, verbose_name="Миниатюра")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'videos_clips'
        verbose_name = "Клип"
        verbose_name_plural = "Клипы"
        indexes = [
            models.Index(fields=['video_file', 'start_offset'], name='vid_clips_vf_start_offset_idx'),
            models.Index(fields=['is_annotated'], name='videos_clips_is_annotated_idx'),
            models.Index(fields=['created_at'], name='vid_clips_created_at_idx'),
        ]
    
    def __str__(self):
        return f"Клип {self.start_offset}-{self.end_offset}с из {self.video_file}"


class VideoAnnotation(models.Model):
    """
    Аннотация к видео (для обучения моделей)
    """
    verbose_name = "Аннотация видео"
    verbose_name_plural = "Аннотации видео"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clip = models.ForeignKey(Clip, on_delete=models.CASCADE, related_name='annotations', verbose_name="Клип")
    label = models.CharField(max_length=255, verbose_name="Метка")
    start_time = models.FloatField(help_text="Время начала в секундах от начала клипа", verbose_name="Время начала")
    end_time = models.FloatField(help_text="Время окончания в секундах от начала клипа", verbose_name="Время окончания")
    bbox = models.JSONField(help_text="Координаты bounding box в формате {'x': 0, 'y': 0, 'w': 0, 'h': 0}", verbose_name="Границы объекта")
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], verbose_name="Уверенность")
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='videos_video_annotations_created_by_user', verbose_name="Создано пользователем")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'В ожидании'),
            ('approved', 'Утверждено'),
            ('rejected', 'Отклонено')
        ],
        default='pending',
        verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'videos_video_annotations'
        verbose_name = "Аннотация видео"
        verbose_name_plural = "Аннотации видео"
        indexes = [
            models.Index(fields=['clip', 'label'], name='vid_annot_clip_label_idx'),
            models.Index(fields=['status'], name='videos_vid_annot_status_idx'),
            models.Index(fields=['created_at'], name='vid_annot_created_at_idx'),
        ]
    
    def __str__(self):
        return f"{self.label} аннотация для {self.clip}"
    
    def get_status_display(self):
        STATUS_CHOICES = [
            ('pending', 'В ожидании'),
            ('approved', 'Утверждено'),
            ('rejected', 'Отклонено')
        ]
        for choice_key, choice_value in STATUS_CHOICES:
            if choice_key == self.status:
                return choice_value
        return self.status