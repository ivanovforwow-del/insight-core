from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets
from .models import MLModel
from cameras.models import Camera, Zone, Line
from events.models import Rule, Event
from videos.models import VideoFile, Clip, VideoAnnotation
from alerts.models import AlertChannel, Alert


class PrettyJSONWidget(widgets.Textarea):
    """Пользовательский виджет для лучшей визуализации JSON в админке"""
    def __init__(self, attrs=None):
        default_attrs = {'cols': '80', 'rows': '20'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        import json
        if value is None or value == '':
            return ''
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                pass
        if isinstance(value, (dict, list)):
            return json.dumps(value, indent=2, ensure_ascii=False)
        return value


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'accuracy', 'is_active', 'created_at']
    list_display_links = ['name']
    list_display_links = ['name']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'version', 'is_active')
        }),
        ('Детали модели', {
            'fields': ('model_file', 'training_dataset_size', 'accuracy')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# Удаляем регистрацию дублирующих моделей, так как они теперь находятся в других приложениях
# Оставляем только MLModel, так как она уникальна для приложения analytics