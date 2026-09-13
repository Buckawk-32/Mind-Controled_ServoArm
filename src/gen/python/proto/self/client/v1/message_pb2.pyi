from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TAG_MESSAGE_UNSPECIFIED: _ClassVar[Tag]
    TAG_ERROR: _ClassVar[Tag]
    TAG_CONNECTION: _ClassVar[Tag]
    TAG_PONG: _ClassVar[Tag]
    TAG_QUIT: _ClassVar[Tag]
TAG_MESSAGE_UNSPECIFIED: Tag
TAG_ERROR: Tag
TAG_CONNECTION: Tag
TAG_PONG: Tag
TAG_QUIT: Tag

class PacketEnvelope(_message.Message):
    __slots__ = ("tag", "client_id", "client_name", "timestamp", "message", "connection", "ping", "error", "quit")
    TAG_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    QUIT_FIELD_NUMBER: _ClassVar[int]
    tag: Tag
    client_id: int
    client_name: str
    timestamp: int
    message: Message
    connection: Connection
    ping: Ping
    error: Error
    quit: Quit
    def __init__(self, tag: _Optional[_Union[Tag, str]] = ..., client_id: _Optional[int] = ..., client_name: _Optional[str] = ..., timestamp: _Optional[int] = ..., message: _Optional[_Union[Message, _Mapping]] = ..., connection: _Optional[_Union[Connection, _Mapping]] = ..., ping: _Optional[_Union[Ping, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ..., quit: _Optional[_Union[Quit, _Mapping]] = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("receiving_id", "message")
    RECEIVING_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    receiving_id: int
    message: str
    def __init__(self, receiving_id: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class Connection(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Ping(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Error(_message.Message):
    __slots__ = ("error",)
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: str
    def __init__(self, error: _Optional[str] = ...) -> None: ...

class Quit(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
