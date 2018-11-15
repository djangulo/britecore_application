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

    def test_can_create_risk(self):
        """Authenticated user should be able to create a risk type."""
        expected = RiskType.objects.first
        url = reverse('risktype-list')
        response = self.client.post(url, data={
                'name': 'Non anonymous risk!',
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

    def test_create_risk_returns_correct_status_code(self):
        """Should return a 201"""
        expected = 201
        url = reverse('risktype-list')
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

    def test_create_risk_returns_correct_code(self):
        """Should return the created name."""
        expected = 'Non anonymous risk!'
        url = reverse('risktype-list')
        response = self.client.post(url, data={
                'name': 'Non anonymous risk!',
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

    def test_can_get_risk_list(self):
        """Should be able to retrieve a list of risks."""
        expected = ['Risk1', 'Risk2']
        url = reverse('risktype-list')
        RiskType.objects.bulk_create([
            RiskType(name='Risk1'),
            RiskType(name='Risk2'),
        ])
        response = self.client.get(url)
        ids = [i['name'] for i in response.data]
        self.assertEqual(
            expected,
            ids,
            '\nDid not retrive correct ids from list, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': ids,
            }
        )

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

    def test_can_edit_risk_with_put(self):
        """Should be able to edit a risk type with a PUT method."""
        expected = 'Risk1 modified'
        risk1 = RiskType.objects.create(name='Risk1')
        url = reverse('risktype-detail', kwargs={'pk': risk1.id})
        response = self.client.put(url, data={'name': 'Risk1 modified'})
        self.assertEqual(
            expected,
            response.data['name'],
            '\nWrong name returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected,
                'got': response.data['name'],
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

    def test_risk_contains_field_type_field_with_fields(self):
        """
        Risk API should contain a 'fields' key, which should be
        populated.
        """
        risk1 = RiskType.objects.create(name='Risk1')
        field1 = FieldType.objects.create(name='Field1',
                                          data_type=0)
        risk1.fields.add(field1)
        risk1.save()
        expected = {
            'id': risk1.id,
            'name': 'Risk1',
            'fields': [{
                'id': field1.id,
                'name': 'Field1',
                'data_type': 0,
            }]
        }
        url = reverse('risktype-detail', kwargs={'pk': risk1.id})
        response = self.client.get(url)
        self.assertEqual(
            expected['fields'],
            response.data['fields'],
            '\nWrong fields returned, expected '
            '%(exp)s, got %(got)s' % {
                'exp': expected['fields'],
                'got': response.data['fields'],
            }
        )

    def test_add_field_action_creates_nonexistent_field(self):
        """
        Should be able to add a field type to a risk type and create
        the field on the fly.
        """
        expected = FieldType.objects.first
        risk1 = RiskType.objects.create(name='Risk1')
        url = reverse('risktype-add-field', kwargs={'pk': risk1.id})
        response = self.client.post(url, data={
            'name': 'Nonexistent_field',
            'data_type': 0,
        })
        self.assertIn(
            expected(),
            risk1.fields.all(),
            '\nField not contained in Risk, expected '
            '%(exp)s, to be in %(got)s' % {
                'exp': expected(),
                'got': risk1.fields.all(),
            }
        )

    def test_add_field_action_assigns_field_if_field_exists(self):
        """
        Should be able to add a field type to a risk type when the passed
        field exists.
        """
        expected = FieldType.objects.first
        risk1 = RiskType.objects.create(name='Risk1')
        field1 = FieldType.objects.create(name='Exisiting field',
                                          data_type=0)
        url = reverse('risktype-add-field', kwargs={'pk': risk1.id})
        response = self.client.post(url, data={
            'name': 'Exisiting field',
            'data_type': 0,
        })
        self.assertIn(
            expected(),
            risk1.fields.all(),
            '\nField not contained in Risk, expected '
            '%(exp)s, to be in %(got)s' % {
                'exp': expected(),
                'got': risk1.fields.all(),
            }
        )

    def test_add_field_action_invalid_data_returns_400(self):
        """
        Should be able to add a field type to a risk type when the passed
        field exists.
        """
        expected = 400
        risk1 = RiskType.objects.create(name='Risk1')
        url = reverse('risktype-add-field', kwargs={'pk': risk1.id})
        response = self.client.post(url, data={
            'name_not_real': 'This will fail',
            'data_type': 0,
        })
        self.assertEqual(
            expected,
            response.status_code,
            '\nField not contained in Risk, expected '
            '%(exp)s, to be in %(got)s' % {
                'exp': expected,
                'got': response.status_code,
            }
        )

    def test_remove_field_action_removes_field(self):
        """
        Should be able to remove a field from it's assigned fields.
        """
        expected = FieldType.objects.first
        risk1 = RiskType.objects.create(name='Risk1')
        field1 = FieldType.objects.create(name='Exisiting field',
                                          data_type=0)
        risk1.fields.add(field1)
        risk1.save()
        url = reverse('risktype-remove-field', kwargs={'pk': risk1.id})
        response = self.client.post(url, data={
            'id': field1.id,
            'name': field1.name,
            'data_type': field1.data_type,
        })
        risk1 = RiskType.objects.get(pk=risk1.id)
        self.assertNotIn(
            expected(),
            risk1.fields.all(),
            '\nField contained in Risk, expected '
            '%(exp)s, not to be in %(got)s' % {
                'exp': expected(),
                'got': risk1.fields.all(),
            }
        )

    def test_create_bulk_fields_if_fields_passed_on_post(self):
        pass


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
