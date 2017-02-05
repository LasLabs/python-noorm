# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .field import FieldBase


class Float(FieldBase):
    """ It defines a field of the `float` data type. """

    type = float

    _slots = {
        'default': 0.0,
    }
