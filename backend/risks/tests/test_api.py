import json
import base64
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.test import override_settings
from rest_framework import status
from rest_framework.test import (
    APITestCase,
    APIClient,
    APIRequestFactory,
    force_authenticate,
)

from django.core.management import call_command

from risks.models import (
    RiskType,
    FieldType,
)


class RisksAPITests(APITestCase):

    def test_can_get_risk_detail(self):
        """Should be able to retrieve a single risk."""
        expected = 'Risk1'
        risk1 = RiskType.objects.create(name='Risk1')
        url = reverse('risktype-detail', kwargs={'pk': risk1.id})
        response = self.client.get(url)
        self.assertEqual(
            expected,
            response.data['name'],
            '\nDid not retrive correct ids from list, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.data,
            }
        )

    def test_can_delete_risk(self):
        """Should be able to delete a risk type."""
        expected = 204
        risk1 = RiskType.objects.create(name='Risk1')
        url = reverse('risktype-detail', kwargs={'pk': risk1.id})
        response = self.client.delete(url)
        self.assertEqual(
            expected,
            response.status_code,
            '\nInvalid code returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.status_code,
            }
        )

    def test_can_edit_risk_with_patch(self):
        """Should be able to edit a risk type with a PATCH method."""
        expected = 'Risk1 modified'
        risk1 = RiskType.objects.create(name='Risk1')
        url = reverse('risktype-detail', kwargs={'pk': risk1.id})
        response = self.client.patch(url, data={'name': 'Risk1 modified'})
        self.assertEqual(
            expected,
            response.data['name'],
            '\nWrong name returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.data['name'],
            }
        )

    def test_risk_contains_field_type_key(self):
        """Risk API should contain a 'fields' key."""
        expected = []
        risk1 = RiskType.objects.create(name='Risk1')
        url = reverse('risktype-detail', kwargs={'pk': risk1.id})
        response = self.client.get(url)
        self.assertEqual(
            expected,
            response.data['fields'],
            '\nWrong key returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.data['fields'],
            }
        )

class FieldAPITests(APITestCase):

    def test_can_create_field(self):
        """Authenticated user should be able to create a field type."""
        expected = FieldType.objects.first
        url = reverse('fieldtype-list')
        response = self.client.post(url, data={
                'name': 'Non anonymous field!',
            },
        )
        self.assertEqual(
            response.data['id'],
            expected().id,
            '\nInvalid id returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': expected().id,
            }
        )

    def test_create_field_returns_correct_status_code(self):
        """Should return a 201"""
        expected = 201
        url = reverse('fieldtype-list')
        response = self.client.post(url, data={
                'name': 'Non anonymous risk!',
            },
        )
        self.assertEqual(
            response.status_code,
            expected,
            '\nInvalid status code returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.status_code,
            }
        )

    def test_create_field_returns_correct_code(self):
        """Should return the created name."""
        expected = 'Non anonymous field!'
        url = reverse('fieldtype-list')
        response = self.client.post(url, data={
                'name': 'Non anonymous field!',
            },
        )
        self.assertEqual(
            response.data['name'],
            expected,
            '\nInvalid status code returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.data['name'],
            }
        )

    def test_can_get_field_list(self):
        """Should be able to retrieve a list of fields."""
        expected = ['Field1', 'Field2']
        url = reverse('fieldtype-list')
        FieldType.objects.bulk_create([
            FieldType(name='Field1'),
            FieldType(name='Field2'),
        ])
        response = self.client.get(url)
        names = [i['name'] for i in response.data]
        self.assertEqual(
            expected,
            names,
            '\nDid not retrive correct names from list, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': names,
            }
        )

    def test_can_get_field_detail(self):
        """Should be able to retrieve a single field."""
        expected = 'Field1'
        field1 = FieldType.objects.create(name='Field1')
        url = reverse('fieldtype-detail', kwargs={'pk': field1.id})
        response = self.client.get(url)
        self.assertEqual(
            expected,
            response.data['name'],
            '\nDid not retrive correct name, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.data,
            }
        )

    def test_can_delete_field(self):
        """Should be able to delete a field type."""
        expected = 204
        field1 = FieldType.objects.create(name='Field1')
        url = reverse('fieldtype-detail', kwargs={'pk': field1.id})
        response = self.client.delete(url)
        self.assertEqual(
            expected,
            response.status_code,
            '\nInvalid code returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.status_code,
            }
        )

    def test_can_edit_field_with_put(self):
        """Should be able to edit a field type with a PUT method."""
        expected = 'Field1 modified'
        field1 = FieldType.objects.create(name='Field1')
        url = reverse('fieldtype-detail', kwargs={'pk': field1.id})
        response = self.client.put(url, data={'name': 'Field1 modified'})
        self.assertEqual(
            expected,
            response.data['name'],
            '\nWrong name returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.data['name'],
            }
        )

    def test_can_edit_field_with_patch(self):
        """Should be able to edit a field type with a PATCH method."""
        expected = 'Field1 modified'
        field1 = FieldType.objects.create(name='Field1')
        url = reverse('fieldtype-detail', kwargs={'pk': field1.id})
        response = self.client.patch(url, data={'name': 'Field1 modified'})
        self.assertEqual(
            expected,
            response.data['name'],
            '\nWrong name returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.data['name'],
            }
        )
