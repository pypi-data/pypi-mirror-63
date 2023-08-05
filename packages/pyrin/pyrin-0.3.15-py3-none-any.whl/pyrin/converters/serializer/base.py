# -*- coding: utf-8 -*-
"""
serializer base module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.utils.singleton import MultiSingletonMeta


class SerializerSingletonMeta(MultiSingletonMeta):
    """
    serializer singleton meta class.
    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class SerializerBase(CoreObject, metaclass=SerializerSingletonMeta):
    """
    serializer base class.
    all application serializers must inherit from this.
    """

    @abstractmethod
    def serialize(self, value, **options):
        """
        serializes the given value.

        :param object value: value to be serialized.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: serialized object.
        """

        raise CoreNotImplementedError()

    def serialize_list(self, values, **options):
        """
        serializes the given list of values.

        :param list[object] values: values to be serialized.

        :returns: list of serialized objects.
        :rtype: list
        """

        if values is None or len(values) == 0:
            return []

        return [self.serialize(value, **options) for value in values]
