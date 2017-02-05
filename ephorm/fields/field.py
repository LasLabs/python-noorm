# -*- coding: utf-8 -*-
# Copyright 2017-TODAY LasLabs Inc.
# License MIT (https://opensource.org/licenses/MIT).

from ..exceptions import FieldFieldValueError


class FieldMeta(type):
    """ FieldBaseMeta provides the metaclass for all field objects. """

    type_map = {}

    def __new__(meta, name, bases, dct):
        """ It combines the ``_slots`` from all bases into ``__slots__``. """
        slots = {}
        for base in reversed(bases):
            slots.update(
                getattr(base, '_slots', {}),
            )
        slots.update(dct.get('_slots', {}))
        dct['__slots__'] = slots
        return type.__new__(meta, name, bases, dct)

    def __init__(self, *args, **kwargs):
        """ It maintains the concept of type & a mapping to fields. """
        super(FieldMeta, self).__init__(*args, **kwargs)
        if not self.type:
            self.type = str
        if self.type not in self.type_map:
            self.type_map[self.type] = self


class FieldBase(object):
    """ FieldBase provides the FieldBase interface definition.

    Arguments:
        default (object|callable): The default value for the field.
            If a `callable` is provided, it will be called with the
            current `FieldBase` instance as the first argument. It should
            return an already instantiated object of the correct type.
        options (list): This is a list of valid options for the field value.
    Attributes:
        _slots (dict): This dictionary can be defined in child classes, which
            will be aggregated into the ``__slots__`` attribute of the current
            class. The aggregation is in reverse base order, so children key
            assignments will take precedence over the parents. The supported
            keys and descriptions are the same as the supported arguments.
        __slots__ (dict): These are the final computed slots for the field.
            This is the attribute that is used when getting/setting slot
            values post instantiation. Note that this variable should never
            be directly accesed, but should instead be accessed using the
            `get_slot` and `set_slots` methods.
    """

    __metaclass__ = FieldMeta

    type = None
    _value = None
    _model = None

    _slots = {
        'default': None,
        'options': None,
    }

    @property
    def value(self):
        return self._value

    def get_object(self, *args, **kwargs):
        """ It returns an object of the correct data type for the args.

        Child classes should override this method in order to customize how
        the data types are created & handled post-creation (such as if the
        object is intensive to create, but less-so to mutate).
        """
        if len(args) == 1 and args[0] is None:
            return self.type()
        return self.type(*args, **kwargs)

    def get_slot(self, name):
        """ It returns the slot option for the name. """
        return self.__slots__.get(name, None)

    def set_value(self, value=None):
        """ It sends the value, or the default value to _set. """
        if value is None:
            value = self.get_slot('default')
        if callable(value):
            value = value(self)
        return self._set(value)

    def _set(self, *args, **kwargs):
        """ It sets the value, type-casted for the field via `get_object`.

        Child classes should override this if specific handling is required
        for the object value when saving to the instance.
        """
        if len(args) == 1 and isinstance(args[0], self.type):
            value = args[0]
        else:
            value = self.get_object(*args, **kwargs)
        if options and value not in options:
            raise FieldValueError(
                '%s is not a valid option (one of %s)' % (
                    value, options,
                )
            )

    def set_slots(self, **kwargs):
        """ It updates the slots with kwargs. """
        self.__slots__.update(**kwargs)

    def initialize(self, model, value=None):
        """ It sets the model relationship"""
        self._model = model
        self.set_value(value)

    def __init__(self, **kwargs):
        """ It initializes the FieldBase. """
        self.set_slots(**kwargs)

    def __proxy_method__(self, method, catch=tuple(), *args, **kwargs):
        """ Proxy a method to the value object when exceptions on super.

        Args:
            method (str): Name of method to call on `superclass` and
                `self.value` in the event of failure.
            catch (tuple): Tuple of exceptions to catch. Exceptions of types
                here will retry the method on `self.value`. If that also
                generates an exception, the original exception will be raised.
            *args (mixed): Positional arguments to pass through to method
                call(s).
            **kwargs (mixed): Keyword arguments to pass through to method
                calls(s).
        """
        super_method = getattr(super(FieldBase, self), method)
        try:
            return super_method(*args, **kwargs)
        except catch as err:
            try:
                return getattr(self.value, method)(*args, **kwargs)
            except (TypeError, AttributeError) + catch:
                raise err

    # Comparison

    def __and__(self, other):
        return self.value and other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __or__(self, other):
        return self.value or other.value

    def __xor__(self, other):
        return self.value ^ other.value

    # Binary Arithmetic

    def __add__(self, other):
        return self.value + other.value

    def __sub__(self, other):
        return self.value - other.value

    def __mul__(self, other):
        return self.value * other.value

    def __div__(self, other):
        return self.value / other.value

    def __mod__(self, other):
        return self.value % other.value

    def __divmod__(self, other):
        return divmod(self.value, other.value)

    def __pow__(self, power, modulo=None):
        return pow(self.value, power, modulo)

    def __lshift__(self, other):
        return self.value << other.value

    def __rshift__(self, other):
        return self.value >> other.value

    # Unary Arithmetic

    def __abs__(self):
        return self.value.__abs__()

    def __invert__(self):
        return ~self.value

    def __neg__(self):
        return -self.value

    def __pos__(self):
        return +self.value

    # Mixed Mode Arithmetic

    def __coerce__(self, other):
        return (self.value, self.type(other.value))

    # Inplace Arithmetic

    def __iadd__(self, other):
        self.value += other.value
        return self.value

    def __iand__(self, other):
        self.value &= other.value
        return self.value

    def __ifloordiv__(self, other):
        self.value //= other.value
        return self.value

    def __ilshift__(self, other):
        self.value <<= other.value
        return self.value

    def __imod__(self, other):
        self.value %= other.value
        return self.value

    def __imul__(self, other):
        self.value *= other.value
        return self.value

    def __ior__(self, other):
        self.value |= other.value
        return self.value

    def __ipow__(self, other):
        self.value **= other.value
        return self.value

    def __irshift__(self, other):
        self.value >>= other.value
        return self.value

    def __isub__(self, other):
        self.value -= other.value
        return self.value

    def __itruediv__(self, other):
        self.value /= other.value
        return self.value

    def __ixor__(self, other):
        self.value ^= other.value
        return self.value

    # Representation

    def __complex__(self):
        return complex(self.value)

    def __float__(self):
        return float(self.value)

    def __hash__(self):
        return hash(self.value)

    def __hex__(self):
        return hex(self.value)

    def __int__(self):
        return int(self.value)

    def __long__(self):
        return long(self.value)

    def __nonzero__(self):
        return self.value and self.value.__nonzero__()

    def __oct__(self):
        return oct(self.value)

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)

    # Mapping

    def __getattr__(self, attr):
        return self.__proxy_method__('__getattr__', (AttributeError, ), attr)

    def __getitem__(self, item):
        return self.__proxy_method__('__getitem__', (KeyError, ), item)

    def __setattr__(self, attr, value):
        return self.__proxy_method__(
            '__setattr__', (AttributeError, ),
            attr, value,
        )

    def __setitem__(self, item, value):
        return self.__proxy_method__(
            '__setitem__', (KeyError, ),
            item, value,
        )
