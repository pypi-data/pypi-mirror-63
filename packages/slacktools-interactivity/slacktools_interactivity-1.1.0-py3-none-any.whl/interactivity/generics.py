from abc import ABC, abstractmethod
from typing import Any, Callable, ClassVar, Dict, Generic, Type, TypeVar, Union

from .exceptions import InteractivityError


class Payload:
    """
    Base payload class. Payload classes are meant to help auto-complete attributes
    without having to reference the Slack docs but the Slack docs only include
    non-exhaustive lists of attributes so this class generically handles
    any non-explicitly identified attributes.
    """

    def __init__(self, **kwargs: Dict[str, Any]):
        self._request_data: Dict[str, Any] = kwargs

    def __getattr__(self, item: str) -> Any:
        """Allows the payload attributes to be directly accessible."""
        if attr := self._request_data.get(item):
            return attr
        return super().__getattribute__(item)


P_co = TypeVar("P_co", bound=Payload, covariant=True)


class ActivityHandler(ABC, Generic[P_co]):
    """
    Base class for handling Slack interactivity requests:
    https://api.slack.com/interactivity
    """

    def __init__(self, payload: P_co):
        self.payload = payload

    @abstractmethod
    def execute(self) -> Union[Dict[str, Any], None]:
        """Implement the activity specific logic here."""
        pass


H_co = TypeVar("H_co", bound=ActivityHandler, covariant=True)


class HandlerFactory(ABC, Generic[H_co]):
    """
    Base factory class for initializing `ActivityHandler` instances from a
    Slack interactivity request.
    """

    _handlers: ClassVar[Union[Dict[str, H_co], None]] = None

    @classmethod
    def register(cls, key: str) -> Callable[[Type[H_co]], Type[H_co]]:
        """
        The decorator used to register a `ActivityHandler` with the factory.

        :param key: The identifier used to reference the handler by the factory.
        """

        def _register(klass: Type[H_co]) -> Type[H_co]:
            cls.register_handler(key, klass)
            return klass

        return _register

    @classmethod
    def register_handler(cls, key: str, klass: Type[H_co]) -> None:
        """
        :param key: The identifier used to reference the handler by the factory.
        :param klass: The `ActivityHandler` class to associate with the key.
        """
        if cls._handlers is None:
            cls._handlers = {}
        if cls._handlers.get(key):
            raise InteractivityError(
                f"{cls.__name__}: {key} has already been registered."
            )
        cls._handlers[key] = klass

    @classmethod
    def make_handler(cls, request_data: Dict[str, Any]) -> H_co:
        """
        :param request_data: The body from the Slack interactivity request.
        """
        payload = cls.make_payload(request_data)
        key = cls.extract_key(payload)
        klass = cls._handlers.get(key) if cls._handlers else None

        if not klass:
            raise InteractivityError(
                f"{cls.__name__}: No registered handler found for {key}"
            )

        return klass(payload)

    @classmethod
    def make_payload(cls, request_data: Dict[str, Any]) -> Payload:
        """
        Initialize and return an `Payload`.

        :param request_data: The Slack interactivity request data.
        """
        return Payload(**request_data)

    @classmethod
    @abstractmethod
    def extract_key(cls, payload: Payload) -> str:
        """
        Extracts the key used to identify which registered handler to initialize.

        :param payload: The `Payload` to extract the key used to register
            handlers with the factory from.
        """
        pass
