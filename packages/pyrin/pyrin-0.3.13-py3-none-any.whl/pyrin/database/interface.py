# -*- coding: utf-8 -*-
"""
database interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.utils.singleton import MultiSingletonMeta


class SessionFactorySingletonMeta(MultiSingletonMeta):
    """
    session factory singleton meta class.
    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractSessionFactoryBase(CoreObject, metaclass=SessionFactorySingletonMeta):
    """
    abstract session factory base class.
    """

    @abstractmethod
    def create_session_factory(self, engine):
        """
        creates a database session factory and binds it to
        given engine and returns it.

        :param Engine engine: database engine.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: database session
        :rtype: Session
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def is_request_bounded(self):
        """
        gets a value indicating that this session factory
        type should be bounded into request.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()
