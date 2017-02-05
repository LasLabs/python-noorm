# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from uuid import uuid4
from .field import FieldBase


class ID(FieldBase):
    """ ID defines a unique identifier for Model records. """

    type = uuid4

    def get_object(self, *args, **kwargs):
        return self.type()
