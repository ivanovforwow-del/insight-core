from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets
from .models import (
    MLModel, Camera, Zone, Line, Rule,
    VideoFile, Clip, VideoAnnotation,
    Event
)
from alerts.models import AlertChannel, Alert


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


@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'version', 'accuracy', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'version', 'is_active')
        }),
        ('Model Details', {
            'fields': ('model_file', 'training_dataset_size', 'accuracy')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'vendor', 'created_at']
    list_filter = ['status', 'vendor', 'created_at']
    search_fields = ['name', 'location', 'rtsp_url']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Camera Information', {
            'fields': ('name', 'location', 'status', 'vendor')
        }),
        ('Stream Configuration', {
            'fields': ('rtsp_url', 'stream_settings')
        }),
        ('Media', {
            'fields': ('snapshot',)
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
    list_display = ['name', 'camera', 'zone_type', 'is_active', 'created_at']
    list_filter = ['zone_type', 'is_active', 'camera']
    search_fields = ['name', 'camera__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Zone Information', {
            'fields': ('name', 'camera', 'zone_type', 'is_active')
        }),
        ('Geometry', {
            'fields': ('polygon',)
        }),
        ('Object Restrictions', {
            'fields': ('allowed_objects', 'forbidden_objects', 'max_objects', 'min_duration')
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
    list_display = ['name', 'camera', 'direction', 'is_active', 'created_at']
    list_filter = ['direction', 'is_active', 'camera']
    search_fields = ['name', 'camera__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Line Information', {
            'fields': ('name', 'camera', 'direction', 'is_active')
        }),
        ('Geometry', {
            'fields': ('points',)
        }),
        ('Object Restrictions', {
            'fields': ('allowed_objects', 'forbidden_objects')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'camera', 'rule_type', 'severity', 'enabled', 'created_at']
    list_filter = ['rule_type', 'severity', 'enabled', 'camera']
    search_fields = ['name', 'camera__name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Rule Information', {
            'fields': ('name', 'description', 'camera', 'rule_type', 'enabled')
        }),
        ('Target', {
            'fields': ('zone', 'line')
        }),
        ('Configuration', {
            'fields': ('conditions', 'severity')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'camera', 'start_time', 'end_time', 'duration', 'created_at']
    list_filter = ['camera', 'start_time', 'created_at']
    search_fields = ['id', 'camera__name', 'storage_path']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Video Information', {
            'fields': ('camera', 'start_time', 'end_time', 'duration')
        }),
        ('File Details', {
            'fields': ('storage_path', 'file_size', 'fps', 'resolution')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin):
    list_display = ['id', 'video_file', 'start_offset', 'end_offset', 'label', 'is_annotated', 'created_at']
    list_filter = ['is_annotated', 'created_at']
    search_fields = ['id', 'label', 'video_file__id']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Clip Information', {
            'fields': ('video_file', 'start_offset', 'end_offset', 'label', 'is_annotated')
        }),
        ('Media', {
            'fields': ('download_url', 'thumbnail')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VideoAnnotation)
class VideoAnnotationAdmin(admin.ModelAdmin):
    list_display = ['id', 'clip', 'label', 'start_time', 'end_time', 'confidence', 'status', 'created_at']
    list_filter = ['label', 'status', 'created_at']
    search_fields = ['id', 'label', 'clip__id', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Annotation Information', {
            'fields': ('clip', 'label', 'start_time', 'end_time', 'confidence', 'status', 'created_by')
        }),
        ('Bounding Box', {
            'fields': ('bbox',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'rule', 'camera', 'object_class', 'timestamp', 'severity', 'resolved', 'created_at']
    list_filter = ['object_class', 'severity', 'resolved', 'timestamp', 'camera']
    search_fields = ['id', 'object_class', 'track_id', 'rule__name', 'camera__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Event Information', {
            'fields': ('rule', 'camera', 'timestamp', 'object_class', 'track_id', 'severity', 'resolved')
        }),
        ('Detection Details', {
            'fields': ('bbox', 'confidence', 'clip')
        }),
        ('Resolution', {
            'fields': ('resolved_at', 'resolved_by'),
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


@admin.register(AlertChannel)
class AlertChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_type', 'enabled', 'created_at']
    list_filter = ['channel_type', 'enabled', 'created_at']
    search_fields = ['name', 'config']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Channel Information', {
            'fields': ('name', 'channel_type', 'enabled')
        }),
        ('Configuration', {
            'fields': ('config', 'schedule')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'channel', 'status', 'sent_at', 'created_at']
    list_filter = ['status', 'sent_at', 'created_at']
    search_fields = ['id', 'event__id', 'channel__name', 'message']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Alert Information', {
            'fields': ('event', 'channel', 'status', 'sent_at')
        }),
        ('Content', {
            'fields': ('message', 'error_message')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )