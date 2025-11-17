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
    verbose_name = "Модель машинного обучения"
    verbose_name_plural = "Модели машинного обучения"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    model_file = models.FileField(upload_to='ml_models/', verbose_name="Файл модели")
    training_dataset_size = models.PositiveIntegerField(default=0, verbose_name="Размер обучающего набора данных")
    accuracy = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Точность модели от 0 до 1",
        verbose_name="Точность"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    version = models.CharField(max_length=50, default='1.0.0', verbose_name="Версия")
    
    class Meta:
        db_table = 'ml_models'
        verbose_name = "Модель машинного обучения"
        verbose_name_plural = "Модели машинного обучения"
        indexes = [
            models.Index(fields=['name', 'is_active']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} (v{self.version})"


# Оставляем только модель MLModel, остальные дублируют модели из других приложений

