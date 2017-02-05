# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from .field import FieldBase
from ..exceptions import FieldValidationError


class Related(FieldBase):
    """ FieldRelated provides the base for a related field. """

    _slots = {
        'comodel': None,
    }

    def __init__(self):
        if not self.get_slot('comodel'):
            raise FieldValidationError(
                '`comodel` is a required attribute for related fields.',
            )
        super(FieldRelated, self).__init__()
