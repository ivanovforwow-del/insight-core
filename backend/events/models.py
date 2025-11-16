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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='events_rules')
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
    zone = models.ForeignKey('cameras.Zone', on_delete=models.SET_NULL, null=True, blank=True, related_name='events_rules')
    line = models.ForeignKey('cameras.Line', on_delete=models.SET_NULL, null=True, blank=True, related_name='events_rules')
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
        db_table = 'events_rules'
        indexes = [
            models.Index(fields=['camera', 'rule_type'], name='events_rules_camera_rule_type_idx'),
            models.Index(fields=['severity', 'enabled'], name='events_rules_severity_enabled_idx'),
            models.Index(fields=['created_at'], name='events_rules_created_at_idx'),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.camera.name}"


class Event(models.Model):
    """
    Событие, зафиксированное аналитикой
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rule = models.ForeignKey(Rule, on_delete=models.CASCADE, related_name='events_events')
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, related_name='events_events')
    timestamp = models.DateTimeField()
    object_class = models.CharField(max_length=100, help_text="Класс обнаруженного объекта")
    track_id = models.CharField(max_length=100, help_text="ID трека объекта")
    bbox = models.JSONField(help_text="Координаты bounding box")
    confidence = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    severity = models.CharField(max_length=20, choices=Rule.severity.field.choices)
    clip = models.ForeignKey(Clip, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_events')
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='events_events_resolved_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'events_events'
        indexes = [
            models.Index(fields=['camera', 'timestamp'], name='events_events_camera_timestamp_idx'),
            models.Index(fields=['rule', 'severity'], name='events_events_rule_severity_idx'),
            models.Index(fields=['resolved', 'timestamp'], name='events_events_resolved_timestamp_idx'),
            GinIndex(fields=['bbox'], name='events_events_bbox_gin'),  # Для поиска по JSON
        ]
    
    def __str__(self):
        return f"{self.object_class} event at {self.timestamp}"