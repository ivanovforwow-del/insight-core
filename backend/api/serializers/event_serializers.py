# serializers/event_serializers.py
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from events.models import Event, Rule


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'rule': _('Правило'),
            'camera': _('Камера'),
            'timestamp': _('Время'),
            'object_class': _('Класс объекта'),
            'track_id': _('ID трека'),
            'bbox': _('Границы объекта'),
            'confidence': _('Уверенность'),
            'severity': _('Уровень серьезности'),
            'clip': _('Клип'),
            'resolved': _('Решено'),
            'resolved_at': _('Время решения'),
            'resolved_by': _('Решено пользователем'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'name': _('Название'),
            'camera': _('Камера'),
            'rule_type': _('Тип правила'),
            'zone': _('Зона'),
            'line': _('Линия'),
            'conditions': _('Условия'),
            'severity': _('Уровень серьезности'),
            'enabled': _('Активно'),
            'description': _('Описание'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
        }

