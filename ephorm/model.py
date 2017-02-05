# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from collections import defaultdict
from uuid import uuid4

from .tools import classproperty
from .fields.field import FieldBase
from .recordset import Recordset


class ModelMeta(type):
    """ ModelMeta provides the metaclass for all model objects. """

    _all_records = defaultdict(Recordset)
    _models = {}

    def __init__(cls, *args, **kwargs):
        """ It maintains a model registry. """
        self._models[cls._name] = cls

    def __call__(cls, *args, **kwargs):
        """ It maintains a concept of the existing records. """
        record = super(ModelMeta, cls)(*args, **kwargs)
        cls._all_records[cls._name].add(record)
        return record


class Model(object):
    """ Model provides a core for all model objects.

    Attributes:
        _fields (dict): Provides a mapping to a model's field objects, keyed
            by field name.
    """

    __metaclass__ = ModelMeta

    _fields = {}

    __id__ = fields.ID()

    @classproperty
    def _records(cls):
        return cls._all_records[cls._name]

    def __init__(self, *args, **kwargs):
        """ It initializes the ModelBase object.

        The main purpose of this method is to setup the relationship in each
        field to its appropriate model & add all the field objects to
        `self._fields`, keyed by field name.
        """
        super(Model, self).__init__()
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if isinstance(attr, FieldBase):
                attr.initialize(self, kwargs.get(attr_name))
                self._fields[attr_name] = attr

    def __setattr__(self, key, value):
        try:
            self._fields[key].set_value(value)
        except KeyError:
            super(Model, self).__setattr__(key, value)

    def __setitem__(self, key, value):
        self._fields[key].set_value(value)

    # CRUD

    def create(self, vals, recordset=None):
        if not recordset:
            recordset = Recordset()
        record = self()

    # Representation

    def __str__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            ', '.join(['%s=%s' % (k, v) for k, v in self.items()]),
        )

    def __repr__(self):
        return self.__str__()
