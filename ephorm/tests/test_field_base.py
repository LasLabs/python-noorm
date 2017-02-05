# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import mock
import unittest

from ..model import Model
from ..fields.field import FieldBase


class FieldTest(FieldBase):
    type = mock.MagicMock()
    _slots = {
        'default': mock.MagicMock,
        'test': 'test',
    }


class TestFieldBase(unittest.TestCase):

    def setUp(self):
        self.field = FieldBase()
        self.field_test = FieldTest()
        self.model = Model()

    def test_field_meta_type_map(self):
        """ It should add field types to type map. """
        self.assertEqual(
            self.field.type_map[str], FieldBase,
        )

    def test_field_meta_slots(self):
        """ It should add aggregate slots correctly. """
        self.assertEqual(
            self.field_test.__slots__['test'], 'test',
        )
        self.assertIs(
            self.field_test.__slots__['default'], None,
        )

    def test_value(self):
        """ It should return the current value. """
        self.field._value = 'test'
        self.assertEqual(self.field.value, 'test')

    def test_get_slot(self):
        """ It should return the slot value. """
        self.assertEqual(
            self.field_test.get_slot('test'), 'test',
        )

    def test_get_slot_none(self):
        """ It should return None if the slot isn't defined. """
        self.assertIs(
            self.field.get_slot('test'), None,
        )

    def test_set_sets(self):
        """ It should set the value to type-casted input. """
        self.field_test.set(None)
        self.assertEqual(self.field_test.value, FieldTest.type())

    def test_set_args(self):
        """ It should correctly pass-thru args to type creation. """
        args = [1, 2]
        kwargs = {'test': 'awewer'}
        self.field_test.set(*args, **kwargs)
        FieldTest.type.assert_has_calls(
            mock.call(),  # This is due to instantiation in class
            mock.call(*args, **kwargs),
        )

    def test_set_slots(self):
        """ It should update __slots__. """
        self.field.set_slots(kwarg=True)
        self.assertTrue(self.field.__slots__['kwarg'])

    def test_initialize_sets_model(self):
        """ It should set the model on the instance. """
        self.field.initialize('model')
        self.assertEqual(self.field._model, 'model')

    def test_initialize_sets_default(self):
        """ It should initialize the default for the record. """
        self.test_field.initialize(None)
        self.assertIsInstance(self.test_field.value, mock.MagicMock)

    def test_initialize_calls_default_with_self(self):
        """ It should initialize the default with self as first arg. """
        self.test_field.initialize(None)
        self.test_field.value.assert_called_once_with(self.test_field)
