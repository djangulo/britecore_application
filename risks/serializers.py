from rest_framework import serializers

from . import models


class FieldTypeSerializer(serializers.ModelSerializer):
    """Serializer for FieldType model."""
    class Meta:
        model = models.FieldType
        fields = ('id', 'name', 'data_type', 'help_text')


class RiskTypeSerializer(serializers.ModelSerializer):
    """Serializer for RiskType model."""
    fields = FieldTypeSerializer(many=True)

    class Meta:
        model = models.RiskType
        fields = ('id', 'name', 'description', 'fields')

    def create(self, validated_data):
        fields_data = validated_data.pop('fields')
        risk, rcreated = models.RiskType.objects.get_or_create(
            **validated_data
        )
        risk.bulk_add_fields(fields_data)
        return risk
