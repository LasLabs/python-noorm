# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).


class ValidationError(EnvironmentError):
    """ ValidationError indicates a generic validation fail. """


class FieldValidationError(ValidationError):
    """ FieldValidationError indicates an issue with field setup. """


class FieldValueError(ValueError):
    """ FieldValueError indicates an issue with the value of a field. """


class RecordsetValueError(ValueError):
    """ RecordsetValueError indicates an issue with the value of a recordset.
    """
