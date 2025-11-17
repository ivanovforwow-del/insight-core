from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets
from .models import AlertChannel, Alert


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


@admin.register(AlertChannel)
class AlertChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_type', 'created_at']
    list_display_links = ['name']
    list_display_links = ['name']
    list_filter = ['channel_type', 'created_at']
    search_fields = ['name', 'channel_type']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'channel_type')
        }),
        ('Конфигурация', {
            'fields': ('config',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['event', 'channel', 'status', 'created_at']
    list_display_links = ['event']
    list_display_links = ['event']
    list_filter = ['status', 'channel', 'created_at']
    search_fields = ['event__id', 'channel__name', 'message']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('event', 'channel', 'status')
        }),
        ('Детали', {
            'fields': ('message', 'delivery_attempts', 'last_delivery_attempt', 'delivery_response')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }