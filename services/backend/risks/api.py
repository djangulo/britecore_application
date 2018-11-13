from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from . import models, serializers


class RiskTypeViewSet(viewsets.ModelViewSet):
    """Viewset for RiskType model."""
    queryset = models.RiskType.objects.all()
    serializer_class = serializers.RiskTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'])
    def add_field(self, request, pk=None):
        risk = self.get_object()
        serializer = serializers.FieldTypeSerializer(data=request.data)
        if serializer.is_valid():
            field, created = models.FieldType.objects.get_or_create(
                name=serializer.data['name'],
                data_type=serializer.data['data_type'],
            )
            risk.fields.add(field)
            if created:
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_field(self, request, pk=None):
        risk = self.get_object()
        serializer = serializers.FieldTypeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                field = models.FieldType.objects.get(
                    name=serializer.data['name'],
                    data_type=serializer.data['data_type']
                )
                risk.remove_field(field)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except models.FieldType.DoesNotExist:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FieldTypeViewSet(viewsets.ModelViewSet):
    """Viewset for FieldType model."""
    queryset = models.FieldType.objects.all()
    serializer_class = serializers.FieldTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
