from django.contrib import admin
from django.db.models import JSONField
from django.forms import widgets
from .models import Rule, Event


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


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'camera', 'rule_type', 'severity', 'enabled', 'created_at']
    list_filter = ['rule_type', 'severity', 'enabled', 'camera', 'created_at']
    search_fields = ['name', 'camera__name', 'rule_type']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'camera', 'rule_type', 'enabled')
        }),
        ('Conditions', {
            'fields': ('conditions',)
        }),
        ('Severity', {
            'fields': ('severity',)
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
    list_display = ['rule', 'camera', 'timestamp', 'object_class', 'severity', 'resolved']
    list_filter = ['object_class', 'severity', 'resolved', 'timestamp', 'camera']
    search_fields = ['rule__name', 'camera__name', 'object_class']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('rule', 'camera', 'object_class', 'severity', 'resolved')
        }),
        ('Tracking', {
            'fields': ('track_id', 'bbox', 'confidence')
        }),
        ('Timestamps', {
            'fields': ('timestamp', 'created_at', 'updated_at'),
        }),
        ('Clip', {
            'fields': ('clip',),
            'classes': ('collapse',)
        }),
    )
    formfield_overrides = {
        JSONField: {'widget': PrettyJSONWidget},
    }