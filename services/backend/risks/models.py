from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


FIELD_TYPE_CHOICES = (
    (0, _('text')),
    (1, _('number')),
    (2, _('date')),
    (3, _('enum')),
)


class RiskType(models.Model):
    """Represents a risk type."""
    name = models.CharField(max_length=255, blank=False)

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
    risk = models.ManyToManyField(
        RiskType,
        related_name='fields',
        blank=True,
    )

    def __str__(self):
        return '%s, type %s' % (self.name, self.get_data_type_display())
