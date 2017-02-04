# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

class ClassProperty(property):
    """ ClassProperty provides an object wrapper for the decorator. """

    def __get__(self, cls, parent):
        return self.fget.__get__(None, parent)()


def classproperty(method):
    """ classproperty provides a decorator for properties at the class level.

    You would use this decorator in the exact same way you would use the core
    `@property`, except that it is meant to describe the class & not the
    instance.

    Returns:
        ClassProperty: Method wrapped in magic.
    """
    return ClassProperty(classmethod(method))
