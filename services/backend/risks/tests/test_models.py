from django.test import TestCase

from risks.models import RiskType, FieldType

TEST_RISK = {
    'name': 'test risk',
}


class FieldTypeTest(TestCase):
    """Tests for field types."""

    @classmethod
    def setUpTestData(cls):
        cls.risk = RiskType.objects.create(name=TEST_RISK['name'])

    def test_can_create(self):
        """Instance should be able to be created."""
        expected = FieldType.objects.first
        ftype = FieldType.objects.create(name='first_name')
        self.assertEqual(
            ftype,
            expected(),
            'The object was not created properly, instead got %s' % ftype
        )

    def test_can_create_with_no_risk(self):
        """Instance should be able to be created without a RiskType."""
        expected = FieldType.objects.first
        ftype = FieldType.objects.create(name='first_name')
        self.assertEqual(
            ftype,
            expected(),
            'FieldType creation without risktype failed: %s' % ftype
        )

    def test_relationship_accessor(self):
        """Instance should be able to be attached to a RiskType."""
        expected = RiskType
        ftype = FieldType.objects.create(name='first_name')
        ftype.risk.set([self.risk])
        self.assertIsInstance(
            ftype.risk.first(),
            expected,
            'FieldType reverse relationship accessor returned wrong object '
            'type, %s' % ftype.risk
        )


class RiskModelTest(TestCase):
    """
    Tests for risk model.
    """

    @classmethod
    def setUpTestData(cls):
        cls.field1 = FieldType.objects.create(name='field1',
                                              data_type=2)
        cls.field2 = FieldType.objects.create(name='field2',
                                              data_type=0)

    def test_can_create_risk(self):
        """
        Risk type should be able to be created.
        """
        expected = RiskType.objects.first
        rtype = RiskType.objects.create(name='first_name')
        self.assertEqual(
            rtype,
            expected(),
            'The object was not created properly, instead got %s' % rtype
        )

    def test_add_field_works_with_int(self):
        """
        Field type should be added to the RiskType via the add_field method
        by using an integer primary key.
        """
        expected = self.field1
        risk = RiskType.objects.create(name=TEST_RISK['name'])
        risk.add_field(self.field1.pk)
        self.assertEqual(
            risk.fields.first(),
            expected,
            'The field type was not added for the risk type, '
            'instead got %s' % risk.fields.first()
        )

    def test_add_field_works_with_str(self):
        """
        Field type should be added to the RiskType via the add_field method
        by using an string primary key.
        """
        expected = self.field1
        risk = RiskType.objects.create(name=TEST_RISK['name'])
        risk.add_field(str(self.field1.pk))
        self.assertEqual(
            risk.fields.first(),
            expected,
            'The field type was not added for the risk type, '
            'instead got %s' % risk.fields.first()
        )

    def test_add_field_works_with_obj(self):
        """
        Field type should be added to the RiskType via the add_field method
        by using an FieldType object.
        """
        expected = self.field1
        risk = RiskType.objects.create(name=TEST_RISK['name'])
        risk.add_field(self.field1)
        self.assertEqual(
            risk.fields.first(),
            expected,
            'The field type was not added for the risk type, '
            'instead got %s' % risk.fields.first()
        )

    def test_remove_field_works_with_int(self):
        """
        Field type should be removed to the RiskType via the add_field method
        by using an integer primary key.
        """
        expected = None
        risk = RiskType.objects.create(name=TEST_RISK['name'])
        risk.add_field(self.field1.pk)
        risk.remove_field(self.field1.pk)
        self.assertEqual(
            risk.fields.first(),
            expected,
            'The field type was not removed for the risk type, '
            'instead got %s' % risk.fields.first()
        )

    def test_remove_field_works_with_str(self):
        """
        Field type should be removed to the RiskType via the add_field method
        by using an string primary key.
        """
        expected = None
        risk = RiskType.objects.create(name=TEST_RISK['name'])
        risk.add_field(str(self.field1.pk))
        risk.remove_field(str(self.field1.pk))
        self.assertEqual(
            risk.fields.first(),
            expected,
            'The field type was not removed for the risk type, '
            'instead got %s' % risk.fields.first()
        )

    def test_remove_field_works_with_obj(self):
        """
        Field type should be removed to the RiskType via the add_field method
        by using an FieldType object.
        """
        expected = None
        risk = RiskType.objects.create(name=TEST_RISK['name'])
        risk.add_field(self.field1)
        risk.remove_field(self.field1)
        self.assertEqual(
            risk.fields.first(),
            expected,
            'The field type was not removed for the risk type, '
            'instead got %s' % risk.fields.first()
        )
