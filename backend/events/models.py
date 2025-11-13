from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.fields import JSONField
from cameras.models import Camera
from videos.models import Clip
from django.contrib.auth.models import User
import uuid


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
    zone = models.ForeignKey('cameras.Zone', on_delete=models.SET_NULL, null=True, blank=True, related_name='rules')
    line = models.ForeignKey('cameras.Line', on_delete=models.SET_NULL, null=True, blank=True, related_name='rules')
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