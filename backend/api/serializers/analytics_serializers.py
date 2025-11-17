from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from analytics.models import MLModel


class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = '__all__'
        # Добавляем метки полей на русском языке
        labels = {
            'name': _('Название'),
            'description': _('Описание'),
            'model_file': _('Файл модели'),
            'training_dataset_size': _('Размер обучающего набора данных'),
            'accuracy': _('Точность'),
            'is_active': _('Активна'),
            'created_at': _('Дата создания'),
            'updated_at': _('Дата обновления'),
            'version': _('Версия'),
        }