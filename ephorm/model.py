# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

import properties

from weakref import WeakSet

from .recordset import Recordset


class Model(properties.HasProperties):
    """ Model provides the base for all model objects. """

    __recordsets__ = WeakSet

    def __init__(self, __recordset__=None, *args, **kwargs):
        if __recordset__ is None:
            __recordset__ = Recordset()
        record = super(Model, self).__init__(*args, **kwargs)
        __recordset__.add(record)
        return record

    def unlink(self):
        for recordset in self.__recordsets__:
            recordset.remove(self)
