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
    verbose_name = "Канал оповещений"
    verbose_name_plural = "Каналы оповещений"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название")
    channel_type = models.CharField(
        max_length=50,
        choices=[
            ('telegram', 'Telegram'),
            ('email', 'Email'),
            ('webhook', 'Webhook'),
            ('sms', 'SMS'),
            ('push', 'Push Notification')
        ],
        verbose_name="Тип канала"
    )
    config = models.JSONField(help_text="Конфигурация канала (токены, адреса и т.д.)", verbose_name="Конфигурация")
    enabled = models.BooleanField(default=True, verbose_name="Активен")
    schedule = models.JSONField(default=dict, blank=True, help_text="Расписание отправки уведомлений", verbose_name="Расписание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'alerts_alert_channels'
        verbose_name = "Канал оповещений"
        verbose_name_plural = "Каналы оповещений"
        indexes = [
            models.Index(fields=['channel_type', 'enabled'], name='alert_chann_type_enabled_idx'),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.channel_type})"
    
    def get_channel_type_display(self):
        CHANNEL_TYPE_CHOICES = [
            ('telegram', 'Telegram'),
            ('email', 'Email'),
            ('webhook', 'Webhook'),
            ('sms', 'SMS'),
            ('push', 'Push Notification')
        ]
        for choice_key, choice_value in CHANNEL_TYPE_CHOICES:
            if choice_key == self.channel_type:
                return choice_value
        return self.channel_type


class Alert(models.Model):
    """
    Оповещение, отправленное по событию
    """
    verbose_name = "Оповещение"
    verbose_name_plural = "Оповещения"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='alerts', verbose_name="Событие")
    channel = models.ForeignKey(AlertChannel, on_delete=models.CASCADE, related_name='alerts', verbose_name="Канал")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'В ожидании'),
            ('sent', 'Отправлено'),
            ('failed', 'Ошибка'),
            ('delivered', 'Доставлено')
        ],
        default='pending',
        verbose_name="Статус"
    )
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Время отправки")
    message = models.TextField(verbose_name="Сообщение")
    error_message = models.TextField(blank=True, verbose_name="Сообщение об ошибке")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'alerts_alerts'
        verbose_name = "Оповещение"
        verbose_name_plural = "Оповещения"
        indexes = [
            models.Index(fields=['event', 'status'], name='alert_event_status_idx'),
            models.Index(fields=['channel', 'status'], name='alert_channel_status_idx'),
            models.Index(fields=['created_at'], name='alert_created_at_idx'),
        ]
    
    def __str__(self):
        return f"Оповещение для {self.event} через {self.channel}"
    
    def get_status_display(self):
        STATUS_CHOICES = [
            ('pending', 'В ожидании'),
            ('sent', 'Отправлено'),
            ('failed', 'Ошибка'),
            ('delivered', 'Доставлено')
        ]
        for choice_key, choice_value in STATUS_CHOICES:
            if choice_key == self.status:
                return choice_value
        return self.status