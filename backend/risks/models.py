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
    slug = models.SlugField(editable=False, unique=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Overwriting save method to implement full_clean()."""
        self.full_clean()
        super(RiskType, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """Overwriting clean method to implement slug-ification."""
        self.slug = slugify(self.name)
        super(RiskType, self).clean(*args, **kwargs)

    def bulk_add_fields(self, fields):
        """
        Add many field types in bulk, setting the calling RiskType
        object as the risk.
        """
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
                        'help_text': field.get('help_text', ''),
                        'display_order': field.get('display_order', 1),
                        'enum_options': field.get('enum_options', ''),
                        'risk': self
                    })
            created_fields = FieldType.objects.bulk_create(
                [FieldType(**field) for field in valid_fields]
            )
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
    slug = models.SlugField(editable=False)
    help_text = models.CharField(max_length=255, blank=True)
    display_order = models.IntegerField(
        default=0,
        help_text=_('Display order for this field within the risk form'
                    '. If two fields have the same order value, it '
                    'will be resolved by the alphabetic order of their'
                    '"name" value.')
    )
    risk = models.ForeignKey(
        RiskType,
        related_name='fields',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    enum_options = models.CharField(
        max_length=1000,
        blank=True,
        default='',
        help_text=_('Helper for enums, comma separated list of desired options')
    )

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return '%s, type %s' % (self.name, self.get_data_type_display())

    def save(self, *args, **kwargs):
        """Overwriting save method to implement full_clean()."""
        self.full_clean()
        super(FieldType, self).save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        """Overwriting clean method to implement slug-ification."""
        self.slug = slugify(self.name)
        super(FieldType, self).clean(*args, **kwargs)
