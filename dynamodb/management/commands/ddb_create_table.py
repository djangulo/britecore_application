import boto3
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--key-schema-definition',
            action='store',
            dest='key_schema_definition',
            required=True,
            metavar=('HASH_ATTR', 'RANGE_ATTR'),
            nargs='+',
            help=_('Attributes to define the Primary Key schema. '
                   'Required. HASH_ATTR and RANGE_ATTR must match '
                   'attributes defined in --attribute-definitions, '
                   'otherwise an error will be raised.'),
        )
        parser.add_argument(
            '-t', '--table-name',
            action='store',
            dest='table_name',
            help=_('Name of table to create. Must match an existing '
                 'risks.RiskType.slug; will raise an error if no '
                 'match is found.'),
            required=True,
        )
        parser.add_argument(
            '--attribute-definitions',
            action='store',
            dest='attribute_definitions',
            help=_('Attribute definitions to apply. Must match '
                   'existing risks.FieldType.slug\'s; will raise an '
                   'error if no match is found for any one of the '
                   ' fields passed.\ne.g. --attribute-definitions '
                   'last_name first_name birth_date'),
            required=True,
            nargs='+',
        )
        parser.add_argument(
            '--region',
            action='store',
            dest='region',
            help=_('AWS availability zone'),
            default=settings.DYNAMODB_SETTINGS.get(
                'DEFAULT_AVAILABILITY_ZONE',
                'us-east-2'
            ),
        )
        parser.add_argument(
            '--provisioned-throughput',
            action='store',
            dest='key_schema_definition',
            required=True,
            metavar=('READ_CAPACITY', 'WRITE_CAPACITY'),
            nargs='*',
            help=_('Attributes to define the Primary Key schema. '
                   'Required. HASH_ATTR and RANGE_ATTR must match '
                   'attributes defined in --attribute-definitions, '
                   'otherwise an error will be raised.'),
        )

    def handle(self, *args, **options):
        client = boto3.client('dynamodb', region_name=options['region'])
        # try:
        #     resp = client.create_table(
        #         TableName=options['table_name'],
        #         KeySchema=[

        #         ]
        #     )
        # for risk in sample_risks:
        #     r, c = RiskType.objects.get_or_create(**risk)
        #     if c:
        #         self.stdout.write(" Creating risk %s..." % r.name, ending="")
        #         self.stdout.write(self.style.SUCCESS(" OK"))
        #     else:
        #         self.stdout.write(" %s exists, skipping..." % r.name, ending="\n")
        #     self.stdout.flush()
        # employee = RiskType.objects.get(name__iexact='Employee risk policy')
        # vehicle = RiskType.objects.get(name__iexact='Vehicle risk policy')
        # for field in sample_fields:
        #     if field['name'] in (
        #         'First name',
        #         'Last name',
        #         'Employee code',
        #         'Birth date',
        #         'Dependents',
        #     ):
        #         f, c = FieldType.objects.get_or_create(risk=employee, **field)
        #     else:
        #         f, c = FieldType.objects.get_or_create(risk=vehicle, **field)
        #     if c:
        #         self.stdout.write(" Creating field %s..." % f.name, ending="")
        #         self.stdout.write(self.style.SUCCESS(" OK"))
        #     else:
        #         self.stdout.write(" %s exists, skipping..." % f.name, ending="\n")
        #     self.stdout.flush()
