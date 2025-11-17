from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets
from .models import VideoFile, Clip, VideoAnnotation


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


@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'camera', 'start_time', 'end_time', 'duration', 'file_size']
    list_display_links = ['id']
    list_display_links = ['id']
    list_filter = ['start_time', 'end_time', 'camera']
    search_fields = ['id', 'camera__name', 'storage_path']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Информация о камере', {
            'fields': ('camera',)
        }),
        ('Временная информация', {
            'fields': ('start_time', 'end_time', 'duration')
        }),
        ('Информация о файле', {
            'fields': ('storage_path', 'file_size', 'fps', 'resolution')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin):
    list_display = ['id', 'video_file', 'start_offset', 'end_offset', 'label', 'is_annotated']
    list_display_links = ['id']
    list_display_links = ['id']
    list_filter = ['is_annotated', 'label', 'video_file__start_time']
    search_fields = ['id', 'video_file__id', 'label']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Видео файл', {
            'fields': ('video_file',)
        }),
        ('Временная информация', {
            'fields': ('start_offset', 'end_offset')
        }),
        ('Детали', {
            'fields': ('label', 'is_annotated')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VideoAnnotation)
class VideoAnnotationAdmin(admin.ModelAdmin):
    list_display = ['clip', 'label', 'start_time', 'confidence', 'created_by']
    list_display_links = ['clip']
    list_display_links = ['clip']
    list_filter = ['label', 'confidence', 'created_by']
    search_fields = ['clip__id', 'label', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Информация о клипе', {
            'fields': ('clip', 'created_by')
        }),
        ('Временная информация', {
            'fields': ('start_time', 'end_time')
        }),
        ('Информация объекте', {
            'fields': ('label', 'bbox', 'confidence')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }