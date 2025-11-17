from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets
from .models import Camera, Zone, Line


class PrettyJSONWidget(widgets.Textarea):
    """Custom widget for better JSON visualization in admin"""
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
    list_filter = ['status', 'vendor', 'created_at']
    search_fields = ['name', 'location', 'vendor']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location', 'vendor', 'status')
        }),
        ('Connection', {
            'fields': ('rtsp_url',)
        }),
        ('Settings', {
            'fields': ('stream_settings', 'snapshot'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
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
    list_filter = ['direction', 'is_active', 'camera']
    search_fields = ['name', 'camera__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'camera', 'direction', 'is_active')
        }),
        ('Geometry', {
            'fields': ('points',)
        }),
        ('Objects', {
            'fields': ('allowed_objects', 'forbidden_objects'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
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
    list_filter = ['zone_type', 'is_active', 'camera']
    search_fields = ['name', 'camera__name', 'zone_type']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'camera', 'zone_type', 'is_active')
        }),
        ('Geometry', {
            'fields': ('polygon',)
        }),
        ('Objects', {
            'fields': ('allowed_objects', 'forbidden_objects', 'max_objects', 'min_duration'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }