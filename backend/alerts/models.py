from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.postgres.indexes import GinIndex
from events.models import Event
from django.contrib.auth.models import User
import uuid


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
    config = models.JSONField(help_text="Конфигурация канала (токены, адреса и т.д.)")
    enabled = models.BooleanField(default=True)
    schedule = models.JSONField(default=dict, blank=True, help_text="Расписание отправки уведомлений")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'alerts_alert_channels'
        indexes = [
            models.Index(fields=['channel_type', 'enabled'], name='alerts_alert_chann_channel_enabled_idx'),
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
        db_table = 'alerts_alerts'
        indexes = [
            models.Index(fields=['event', 'status'], name='alerts_alerts_event_status_idx'),
            models.Index(fields=['channel', 'status'], name='alerts_alerts_channel_status_idx'),
            models.Index(fields=['created_at'], name='alerts_alerts_created_at_idx'),
        ]
    
    def __str__(self):
        return f"Alert for {self.event} via {self.channel}"