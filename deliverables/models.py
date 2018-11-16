from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models, transaction, connection
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


FIELD_TYPE_CHOICES = (
    (0, _('text')),
    (1, _('number')),
    (2, _('date')),
    (3, _('enum')),
)


class RiskType(models.Model):
    """Represents a risk type."""
    name = models.CharField(max_length=255, blank=False)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name

    def bulk_add_fields(self, fields):
        """Add many field types in bulk."""
        valid_fields = []
        existing_fields = []
        to_be_created_fields = []
        try:
            iter(fields)
            for field in fields:
                if 'name' in field.keys() and 'data_type' in field.keys():
                    valid_fields.append({
                        'name': field['name'],
                        'data_type': field['data_type'],
                        'number_of_fields': field.get('number_of_fields', 1),
                    })
            for field in valid_fields:
                if FieldType.objects.filter(
                    name=field['name'],
                    data_type=field['data_type'],
                    number_of_fields=field.get('number_of_fields', 1),
                ).exists():
                    existing_fields.append(FieldType.objects.get(
                        name=field['name'],
                        data_type=field['data_type'],
                        number_of_fields=field.get('number_of_fields', 1),
                    ))
                else:
                    to_be_created_fields.append(field)
            created_fields = FieldType.objects.bulk_create(
                [FieldType(**field) for field in to_be_created_fields]
            )
            existing_fields.extend(created_fields)
            with transaction.atomic():
                self.fields.add(*existing_fields)
        except TypeError:
            raise ValidationError(
                'Invalid type; arg passed is not iterable: %(arg)s' % {
                    'arg': type(fields),
                })


class FieldType(models.Model):
    """Represents a field type."""
    name = models.CharField(max_length=255, blank=False)
    data_type = models.IntegerField(choices=FIELD_TYPE_CHOICES, default=0,
                                    blank=False)
    help_text = models.CharField(max_length=255, blank=True)
    number_of_fields = models.PositiveSmallIntegerField(
        blank=True,
        default=1,
        help_text=_('Enum (data_type==3) only. Number of fields to display'),
        validators=[MaxValueValidator(10)],
    )
    risk = models.ForeignKey(
        RiskType,
        related_name='fields',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return '%s, type %s' % (self.name, self.get_data_type_display())
