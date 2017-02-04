# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .field import FieldBase


class Int(FieldBase):
    """ It defines a field of the `int` data type. """

    type = int

    _slots = {
        'default': 0,
    }
