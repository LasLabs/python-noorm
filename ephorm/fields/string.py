# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .field import FieldBase


class String(FieldBase):
    """ It defines a field of the `str` data type. """

    type = str

    _slots = {
        'default': '',
        'encoding': 'utf-8',
    }

    def get_object(self, *args, **kwargs):
        if args is None:
            return None
        return self.type(*args, **kwargs).encode(
            self.get_slot('encoding'),
        )
