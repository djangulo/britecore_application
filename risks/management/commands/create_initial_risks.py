from django.core.management.base import BaseCommand
from risks.models import RiskType, FieldType

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
    },
    {
        'name': 'Last name',
        'data_type': 0,
    },
    {
        'name': 'Employee code',
        'data_type': 1,
    },
    {
        'name': 'Birth date',
        'data_type': 2,
    },
    {
        'name': 'Purchase date',
        'data_type': 2,
        'help_text': 'Date the vehicle was acquired.'
    },
    {
        'name': 'Dependents',
        'data_type': 3,
        'help_text': 'Comma separated list of each one of your dependents (i.e. children, parents, etc.).'
    },
    {
        'name': 'Age',
        'data_type': 1,
    },
    {
        'name': 'Vehicle type',
        'data_type': 1,
        'help_text': '0: hatchback, 1: sedan, 2: SUV, 3: Pickup, 4: Sports car, 5: Luxury, 6: Commercial'
    },
    {
        'name': 'Owner',
        'data_type': 0,
        'help_text': 'Full name of vehicle legal owner.',
    },
    {
        'name': 'Vehicle year',
        'data_type': 1,
        'help_text': 'Year of manufacture.',
    },
    {
        'name': 'Chassis ID',
        'data_type': 0,
        'help_text': '15 digit chassis ID.',
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
        for field in sample_fields:
            f, c = FieldType.objects.get_or_create(**field)
            if c:
                self.stdout.write(" Creating field %s..." % f.name, ending="")
                self.stdout.write(self.style.SUCCESS(" OK"))
            else:
                self.stdout.write(" %s exists, skipping..." % f.name, ending="\n")
            self.stdout.flush()
        employee = RiskType.objects.get(name__iexact='Employee risk policy')
        vehicle = RiskType.objects.get(name__iexact='Vehicle risk policy')
        employee.fields.add(
            FieldType.objects.get(name__iexact='First name'),
            FieldType.objects.get(name__iexact='Last name'),
            FieldType.objects.get(name__iexact='Employee code'),
            FieldType.objects.get(name__iexact='Birth date'),
        )
        vehicle.fields.add(
            FieldType.objects.get(name__iexact='Owner'),
            FieldType.objects.get(name__iexact='Vehicle type'),
            FieldType.objects.get(name__iexact='Vehicle year'),
            FieldType.objects.get(name__iexact='Purchase date'),
            FieldType.objects.get(name__iexact='Chassis ID'),
        )
