# serializers/alert_serializers.py
from rest_framework import serializers
from alerts.models import Alert, AlertChannel


class AlertChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertChannel
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'