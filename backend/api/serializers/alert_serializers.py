# serializers/alert_serializers.py
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from alerts.models import Alert, AlertChannel


class AlertChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertChannel
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'name': _('Название'),
            'channel_type': _('Тип канала'),
            'config': _('Конфигурация'),
            'enabled': _('Активен'),
            'schedule': _('Расписание'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'event': _('Событие'),
            'channel': _('Канал'),
            'status': _('Статус'),
            'sent_at': _('Время отправки'),
            'message': _('Сообщение'),
            'error_message': _('Сообщение об ошибке'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }