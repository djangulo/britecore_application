from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _


FIELD_TYPE_CHOICES = (
    (0, _('text')),
    (1, _('number')),
    (2, _('date')),
    (3, _('enum')),
)



class RiskType(models.Model):
    """Represents a risk type."""
    name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name

    def add_field(self, field):
        """
        Adds a field to the objects field set (fields).

        Keyword arguments:
        field -- field pk or FieldType instance to add
        """
        if isinstance(field, int):
            try:
                field = FieldType.objects.get(pk=field)
            except FieldType.DoesNotExist:
                raise FieldType.DoesNotExist(
                    'The primary key passed did not return an object, key: '
                    '%s' % field
                )
        if isinstance(field, str):
            try:
                field = FieldType.objects.get(pk=int(field))
            except ValueError:
                raise ValidationError('Invalid key passed: %s' % field)
            except FieldType.DoesNotExist:
                raise FieldType.DoesNotExist(
                    'The primary key passed did not return an object, key: '
                    '%s' % field
                )
        self.fields.add(field)

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
                    })
            for field in valid_fields:
                if FieldType.objects.filter(
                    name=field['name'],
                    data_type=field['data_type'],
                ).exists():
                    existing_fields.append(FieldType.objects.get(
                        name=field['name'],
                        data_type=field['data_type'],
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

    def remove_field(self, field):
        """
        Removes a field from the objects field set (fields).

        Keyword arguments:
        field -- field pk, str or FieldType instance to remove
        """
        if isinstance(field, int):
            try:
                field = FieldType.objects.get(pk=field)
            except FieldType.DoesNotExist:
                raise FieldType.DoesNotExist(
                    'The primary key passed did not return an object, key: '
                    '%s' % field
                )
        if isinstance(field, str):
            try:
                field = FieldType.objects.get(pk=int(field))
            except ValueError:
                raise ValidationError('Invalid key passed: %s' % field)
            except FieldType.DoesNotExist:
                raise FieldType.DoesNotExist(
                    'The primary key passed did not return an object, key: '
                    '%s' % field
                )
        if field in self.fields.all():
            self.fields.remove(field)


class FieldType(models.Model):
    """Represents a field type."""
    name = models.CharField(max_length=255, blank=False)
    data_type = models.IntegerField(choices=FIELD_TYPE_CHOICES, default=0,
                                    blank=False)
    help_text = models.CharField(max_length=255, blank=True)
    risk = models.ManyToManyField(
        RiskType,
        related_name='fields',
        blank=True,
    )

    class Meta:
        unique_together = ('name', 'data_type')

    def __str__(self):
        return '%s, type %s' % (self.name, self.get_data_type_display())
