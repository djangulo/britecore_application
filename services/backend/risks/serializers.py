from rest_framework import serializers

from . import models


class FieldTypeSerializer(serializers.ModelSerializer):
    """Serializer for FieldType model."""
    class Meta:
        model = models.FieldType
        fields = ('id', 'name', 'data_type')


class RiskTypeSerializer(serializers.ModelSerializer):
    """Serializer for RiskType model."""
    fields = FieldTypeSerializer(many=True, read_only=True)

    class Meta:
        model = models.RiskType
        fields = ('id', 'name', 'fields')
