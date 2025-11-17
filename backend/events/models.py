from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from cameras.models import Camera
from videos.models import Clip
from django.contrib.auth.models import User
import uuid


class Rule(models.Model):
    """
    Правило аналитики (условия срабатывания)
    """
    verbose_name = "Правило"
    verbose_name_plural = "Правила"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название")
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='events_rules', verbose_name="Камера")
    rule_type = models.CharField(
        max_length=50,
        choices=[
            ('line_crossing', 'Пересечение линии'),
            ('zone_violation', 'Нарушение зоны'),
            ('behavior_detection', 'Обнаружение поведения'),
            ('loitering', 'Задержка в зоне'),
            ('object_left_behind', 'Объект оставлен'),
            ('speed_detection', 'Обнаружение скорости'),
            ('counting', 'Подсчет'),
            ('custom', 'Пользовательское правило')
        ],
        verbose_name="Тип правила"
    )
    zone = models.ForeignKey('cameras.Zone', on_delete=models.SET_NULL, null=True, blank=True, related_name='events_rules', verbose_name="Зона")
    line = models.ForeignKey('cameras.Line', on_delete=models.SET_NULL, null=True, blank=True, related_name='events_rules', verbose_name="Линия")
    conditions = models.JSONField(default=dict, help_text="Условия срабатывания правила", verbose_name="Условия")
    severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Низкий'),
            ('medium', 'Средний'),
            ('high', 'Высокий'),
            ('critical', 'Критический')
        ],
        default='medium',
        verbose_name="Уровень серьезности"
    )
    enabled = models.BooleanField(default=True, verbose_name="Активно")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'events_rules'
        verbose_name = "Правило"
        verbose_name_plural = "Правила"
        indexes = [
            models.Index(fields=['camera', 'rule_type'], name='events_rules_cam_rule_type_idx'),
            models.Index(fields=['severity', 'enabled'], name='ev_rules_severity_enabled_idx'),
            models.Index(fields=['created_at'], name='events_rules_created_at_idx'),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"
    
    def get_rule_type_display(self):
        RULE_TYPE_CHOICES = [
            ('line_crossing', 'Пересечение линии'),
            ('zone_violation', 'Нарушение зоны'),
            ('behavior_detection', 'Обнаружение поведения'),
            ('loitering', 'Задержка в зоне'),
            ('object_left_behind', 'Объект оставлен'),
            ('speed_detection', 'Обнаружение скорости'),
            ('counting', 'Подсчет'),
            ('custom', 'Пользовательское правило')
        ]
        for choice_key, choice_value in RULE_TYPE_CHOICES:
            if choice_key == self.rule_type:
                return choice_value
        return self.rule_type


class Event(models.Model):
    """
    Событие, зафиксированное аналитикой
    """
    verbose_name = "Событие"
    verbose_name_plural = "События"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='events_events', verbose_name="Правило")
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='events_events', verbose_name="Камера")
    timestamp = models.DateTimeField(verbose_name="Время")
    object_class = models.CharField(max_length=100, help_text="Класс обнаруженного объекта", verbose_name="Класс объекта")
    track_id = models.CharField(max_length=100, help_text="ID трека объекта", verbose_name="ID трека")
    bbox = models.JSONField(help_text="Координаты bounding box", verbose_name="Границы объекта")
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], verbose_name="Уверенность")
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
        ('critical', 'Критический')
    ], verbose_name="Уровень серьезности")
    clip = models.ForeignKey(Clip, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_events', verbose_name="Клип")
    resolved = models.BooleanField(default=False, verbose_name="Решено")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Время решения")
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_events_resolved_by_user', verbose_name="Решено пользователем")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'events_events'
        verbose_name = "Событие"
        verbose_name_plural = "События"
        indexes = [
            models.Index(fields=['camera', 'timestamp'], name='ev_events_cam_timestamp_idx'),
            models.Index(fields=['rule', 'severity'], name='ev_events_rule_severity_idx'),
            models.Index(fields=['resolved', 'timestamp'], name='ev_events_res_tstamp_idx'),
            GinIndex(fields=['bbox'], name='events_events_bbox_gin'),  # Для поиска по JSON
        ]
    
    def __str__(self):
        return f"{self.object_class} событие в {self.timestamp}"
    
    def get_severity_display(self):
        SEVERITY_CHOICES = [
            ('low', 'Низкий'),
            ('medium', 'Средний'),
            ('high', 'Высокий'),
            ('critical', 'Критический')
        ]
        for choice_key, choice_value in SEVERITY_CHOICES:
            if choice_key == self.severity:
                return choice_value
        return self.severity