# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import operator
import properties

from collections import Iterable, MutableSet

from .model import Model
from .exceptions import RecordsetValueError


OPERATOR_MAP = {
    '>': operator.gt,
    '>=': operator.gte,
    '=': operator.eq,
    '==': operator.eq,
    '<': operator.lt,
    '<=': operator.lte,
}


class Recordset(MutableSet):

    type = None

    def __init__(self, data=None):
        """ It initializes the Recordset. """
        self.data = set()
        if data:
            for row in data:
                self.add(row)

    def add(self, records):
        """ Add a Record (instantiated Model) or Recordset to the collection.

        Args:
            record (HasProperties|Recordset): A model instance or iterator of
                model instances that will be added to the collection. Note that
                all models must be of the same data type as the first record
                inserted into the collection.
        """
        if isinstance(record, Recordset):
            return [self.add(record) for record in records]
        if not self.type:
            self.initialize(records)
        if not isinstance(records, self.type):
            raise RecordsetValueError(
                'A Recordset may not contain Models of disparate types.',
            )
        result = self.data.add(records)
        records.__recordsets__.add(self)
        return result

    def clear(self):
        return self.data.clear()

    def discard(self, value):
        return self.data.discard(value)

    def initialize(self, record):
        if not isinstance(record, Model):
            raise RecordsetValueError(
                'A Recordset may only contain objects inherited from Model.',
            )
        self.type = record.__class__

    def isdisjoint(self, other):
        return self.data.isdisjoint(other)

    def pop(self):
        return self.data.pop()

    def remove(self, value):
        return self.data.remove(value)

    # CRUD

    def create(self, vals):
        """ It creates a new record & adds to the collection.

        Args:
            vals (dict): Dictionary of values to send to Model create.
        Returns:
            Model: The newly created record.
        """
        self.type(__recordset__=self, **vals)

    def search(self, domain):
        """ It searches existing records for conditions in domain.

        Args:
            domain (iter of iter): Iterator of iterators containing strings
                representing a domain. Example::
                    [('int_field_name', '>=', 10)]
        """
        records = self.data or self.type._records
        for field, op, value in domain:
            op = OPERATOR_MAP[op]
            records = filter(
                lambda r: op(getattr(r, field), value),
                records,
            )
        return records

    def unlink(self, record):
        """ Alias for remove. """
        return self.remove(record)

    # Helpers

    def filtered(self, method):
        return self.__class__(
            filter(method, self),
        )

    # Interface

    def __contains__(self, item):
        return self.data.contains(item)

    def __iter__(self):
        for i in self.data:
            yield i
        raise StopIteration()

    def __len__(self):
        return len(self.data)

    # Comparison

    def __le__(self, other):
        return self.data <= other.data

    def __lt__(self, other):
        return self.data < other.data

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.data != other.data

    def __ge__(self, other):
        return self.data >= other.data

    def __gt__(self, other):
        return self.data > other.data

    def __and__(self, other):
        return self.data and other.data

    def __or__(self, other):
        return self.data or other.data

    def __xor__(self, other):
        return self.data ^ other.data

    # Arithmetic

    def __sub__(self, other):
        return self.data - other.data

    # Inplace Arithmetic

    def __iadd__(self, other):
        self.data += other.data

    def __iand__(self, other):
        self.data &= other.data

    def __ixor__(self, other):
        self.data ^= other.data

    def __isub__(self, other):
        self.data -= other.data
