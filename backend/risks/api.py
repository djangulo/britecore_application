from django.core.management import call_command
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from . import models, serializers


class RiskTypeViewSet(viewsets.ModelViewSet):
    """Viewset for RiskType model."""
    queryset = models.RiskType.objects.all()
    serializer_class = serializers.RiskTypeSerializer

    @action(detail=True, methods=['post'])
    def add_field(self, request, pk=None):
        """
        Creates a FieldType and adds the RiskType as the risk field.
        Returns the RistType object with all FieldTypes..
        """
        risk = self.get_object()
        response_data = serializers.RiskTypeSerializer(risk).data
        serializer = serializers.FieldTypeSerializer(data=request.data)
        if serializer.is_valid():
            field, created = models.FieldType.objects.create(
                name=serializer.data['name'],
                data_type=serializer.data['data_type'],
                help_text=serializer.data['help_text'],
                number_of_fields=serializer.data.get('number_of_fields', 1),
                display_order=serializer.data.get('display_order', 1),
                risk=risk
            )
            if created:
                return Response(response_data,
                                status=status.HTTP_201_CREATED)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_field(self, request, pk=None):
        """
        Deletes the FieldType passed in the data from the RiskType
        object.
        Returns the RiskType object with all remaining fields.
        """
        risk = self.get_object()
        response_data = serializers.RiskTypeSerializer(risk).data
        serializer = serializers.FieldTypeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if 'id' in serializer.data.keys():
                    field = models.FieldType.objects.get(pk=serializer.data['id'])
                else:
                    field = models.FieldType.objects.get(
                        name=serializer.data['name'],
                        data_type=serializer.data['data_type'],
                        help_text=serializer.data['help_text'],
                        number_of_fields=serializer.data.get('number_of_fields', 1),
                        display_order=serializer.data.get('display_order', 1),
                    )
                field.delete()
                return Response(response_data, status=status.HTTP_200_OK)
            except models.FieldType.DoesNotExist:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get','post'])
    def create_initial_risks(self, request, pk=None):
        """
        Runs the "create_initial_risks" command, called from the API.
        This allows the user to reset the risks without having to go
        into the python console.
        """
        try:
            data = call_command('create_initial_risks')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FieldTypeViewSet(viewsets.ModelViewSet):
    """Viewset for FieldType model."""
    queryset = models.FieldType.objects.all()
    serializer_class = serializers.FieldTypeSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
