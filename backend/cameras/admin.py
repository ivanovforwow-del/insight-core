from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets
from .models import Camera, Zone, Line


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


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'vendor', 'created_at']
    list_display_links = ['name']
    list_display_links = ['name']
    list_filter = ['status', 'vendor', 'created_at']
    search_fields = ['name', 'location', 'vendor']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'location', 'vendor', 'status')
        }),
        ('Подключение', {
            'fields': ('rtsp_url',)
        }),
        ('Настройки', {
            'fields': ('stream_settings', 'snapshot'),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ['name', 'camera', 'direction', 'is_active']
    list_display_links = ['name']
    list_display_links = ['name']
    list_filter = ['direction', 'is_active', 'camera']
    search_fields = ['name', 'camera__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'camera', 'direction', 'is_active')
        }),
        ('Геометрия', {
            'fields': ('points',)
        }),
        ('Объекты', {
            'fields': ('allowed_objects', 'forbidden_objects'),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'camera', 'zone_type', 'is_active']
    list_display_links = ['name']
    list_display_links = ['name']
    list_filter = ['zone_type', 'is_active', 'camera']
    search_fields = ['name', 'camera__name', 'zone_type']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'camera', 'zone_type', 'is_active')
        }),
        ('Геометрия', {
            'fields': ('polygon',)
        }),
        ('Объекты', {
            'fields': ('allowed_objects', 'forbidden_objects', 'max_objects', 'min_duration'),
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }