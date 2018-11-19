import json
from django.core.management.base import BaseCommand
from risks.models import RiskType, FieldType
from risks.serializers import RiskTypeSerializer

sample_risks = [
    {
        'name': 'Employee risk policy',
        'description': 'Describes the fields for an employee risk policy.'
    },
    {
        'name': 'Vehicle risk policy',
        'description': 'This one represents a vehicle risk policy.'
    },
    {
        'name': 'Empty risk policy',
        'description': 'This risk policy does not contain any fields.'
    }
]
sample_fields = [
    {
        'name': 'First name',
        'data_type': 0,
        'display_order': 0
    },
    {
        'name': 'Last name',
        'data_type': 0,
        'display_order': 1,
    },
    {
        'name': 'Employee code',
        'data_type': 1,
        'display_order': 2,
    },
    {
        'name': 'Birth date',
        'data_type': 2,
        'display_order': 3
    },
    {
        'name': 'Dependents',
        'data_type': 3,
        'help_text': 'Comma separated list of each one of your dependents (i.e. children, parents, etc.).',
        'display_order': 4,
    },
    {
        'name': 'Owner',
        'data_type': 0,
        'help_text': 'Full name of vehicle legal owner.',
        'display_order': 0,
    },
    {
        'name': 'Age',
        'data_type': 1,
        'display_order': 1,
    },
    {
        'name': 'Purchase date',
        'data_type': 2,
        'help_text': 'Date the vehicle was acquired.',
        'display_order': 2,
    },
    {
        'name': 'Vehicle type',
        'data_type': 1,
        'help_text': '0: hatchback, 1: sedan, 2: SUV, 3: Pickup, 4: Sports car, 5: Luxury, 6: Commercial',
        'display_order': 3,
    },
    {
        'name': 'Vehicle year',
        'data_type': 1,
        'help_text': 'Year of manufacture.',
        'display_order': 4,
    },
    {
        'name': 'Chassis ID',
        'data_type': 0,
        'help_text': '15 digit chassis ID.',
        'display_order': 5,
    },
]

class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for risk in sample_risks:
            r, c = RiskType.objects.get_or_create(**risk)
            if c:
                self.stdout.write(" Creating risk %s..." % r.name, ending="")
                self.stdout.write(self.style.SUCCESS(" OK"))
            else:
                self.stdout.write(" %s exists, skipping..." % r.name, ending="\n")
            self.stdout.flush()
        employee = RiskType.objects.get(name__iexact='Employee risk policy')
        vehicle = RiskType.objects.get(name__iexact='Vehicle risk policy')
        empty = RiskType.objects.get(name__iexact='Empty risk policy')
        for field in sample_fields:
            if field['name'] in (
                'First name',
                'Last name',
                'Employee code',
                'Birth date',
                'Dependents',
            ):
                f, c = FieldType.objects.get_or_create(risk=employee, **field)
            else:
                f, c = FieldType.objects.get_or_create(risk=vehicle, **field)
            if c:
                self.stdout.write(" Creating field %s..." % f.name, ending="")
                self.stdout.write(self.style.SUCCESS(" OK"))
            else:
                self.stdout.write(" %s exists, skipping..." % f.name, ending="\n")
            self.stdout.flush()
        _employee = RiskTypeSerializer(employee).data
        _vehicle = RiskTypeSerializer(vehicle).data
        _empty = RiskTypeSerializer(empty).data
        return json.dumps([_employee, _vehicle, _empty])
