# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: minknow/rpc/keystore.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from minknow.rpc import rpc_options_pb2 as minknow_dot_rpc_dot_rpc__options__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='minknow/rpc/keystore.proto',
  package='ont.rpc.keystore',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1aminknow/rpc/keystore.proto\x12\x10ont.rpc.keystore\x1a\x19google/protobuf/any.proto\x1a\x1dminknow/rpc/rpc_options.proto\"\xc3\x01\n\x0cStoreRequest\x12@\n\x06values\x18\x01 \x03(\x0b\x32*.ont.rpc.keystore.StoreRequest.ValuesEntryB\x04\x88\xb5\x18\x01\x12,\n\x08lifetime\x18\x02 \x01(\x0e\x32\x1a.ont.rpc.keystore.Lifetime\x1a\x43\n\x0bValuesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12#\n\x05value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any:\x02\x38\x01\"\x0f\n\rStoreResponse\";\n\rRemoveRequest\x12\x13\n\x05names\x18\x01 \x03(\tB\x04\x88\xb5\x18\x01\x12\x15\n\rallow_missing\x18\x02 \x01(\x08\"\x10\n\x0eRemoveResponse\"#\n\rGetOneRequest\x12\x12\n\x04name\x18\x01 \x01(\tB\x04\x88\xb5\x18\x01\"5\n\x0eGetOneResponse\x12#\n\x05value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\"2\n\nGetRequest\x12\r\n\x05names\x18\x01 \x03(\t\x12\x15\n\rallow_missing\x18\x02 \x01(\x08\"\x8d\x01\n\x0bGetResponse\x12\x39\n\x06values\x18\x01 \x03(\x0b\x32).ont.rpc.keystore.GetResponse.ValuesEntry\x1a\x43\n\x0bValuesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12#\n\x05value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any:\x02\x38\x01\":\n\x0cWatchRequest\x12\x13\n\x05names\x18\x01 \x03(\tB\x04\x88\xb5\x18\x01\x12\x15\n\rallow_missing\x18\x02 \x01(\x08\"\xa9\x01\n\rWatchResponse\x12;\n\x06values\x18\x01 \x03(\x0b\x32+.ont.rpc.keystore.WatchResponse.ValuesEntry\x12\x16\n\x0eremoved_values\x18\x02 \x03(\t\x1a\x43\n\x0bValuesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12#\n\x05value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any:\x02\x38\x01*Y\n\x08Lifetime\x12\x1d\n\x19UNTIL_NEXT_PROTOCOL_START\x10\x00\x12\x16\n\x12UNTIL_PROTOCOL_END\x10\x01\x12\x16\n\x12UNTIL_INSTANCE_END\x10\x02\x32\x90\x03\n\x0fKeyStoreService\x12J\n\x05store\x12\x1e.ont.rpc.keystore.StoreRequest\x1a\x1f.ont.rpc.keystore.StoreResponse\"\x00\x12M\n\x06remove\x12\x1f.ont.rpc.keystore.RemoveRequest\x1a .ont.rpc.keystore.RemoveResponse\"\x00\x12N\n\x07get_one\x12\x1f.ont.rpc.keystore.GetOneRequest\x1a .ont.rpc.keystore.GetOneResponse\"\x00\x12\x44\n\x03get\x12\x1c.ont.rpc.keystore.GetRequest\x1a\x1d.ont.rpc.keystore.GetResponse\"\x00\x12L\n\x05watch\x12\x1e.ont.rpc.keystore.WatchRequest\x1a\x1f.ont.rpc.keystore.WatchResponse\"\x00\x30\x01\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,minknow_dot_rpc_dot_rpc__options__pb2.DESCRIPTOR,])

_LIFETIME = _descriptor.EnumDescriptor(
  name='Lifetime',
  full_name='ont.rpc.keystore.Lifetime',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNTIL_NEXT_PROTOCOL_START', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNTIL_PROTOCOL_END', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UNTIL_INSTANCE_END', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=920,
  serialized_end=1009,
)
_sym_db.RegisterEnumDescriptor(_LIFETIME)

Lifetime = enum_type_wrapper.EnumTypeWrapper(_LIFETIME)
UNTIL_NEXT_PROTOCOL_START = 0
UNTIL_PROTOCOL_END = 1
UNTIL_INSTANCE_END = 2



_STOREREQUEST_VALUESENTRY = _descriptor.Descriptor(
  name='ValuesEntry',
  full_name='ont.rpc.keystore.StoreRequest.ValuesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ont.rpc.keystore.StoreRequest.ValuesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ont.rpc.keystore.StoreRequest.ValuesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=235,
  serialized_end=302,
)

_STOREREQUEST = _descriptor.Descriptor(
  name='StoreRequest',
  full_name='ont.rpc.keystore.StoreRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='ont.rpc.keystore.StoreRequest.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\210\265\030\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='lifetime', full_name='ont.rpc.keystore.StoreRequest.lifetime', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_STOREREQUEST_VALUESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=302,
)


_STORERESPONSE = _descriptor.Descriptor(
  name='StoreResponse',
  full_name='ont.rpc.keystore.StoreResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=304,
  serialized_end=319,
)


_REMOVEREQUEST = _descriptor.Descriptor(
  name='RemoveRequest',
  full_name='ont.rpc.keystore.RemoveRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='names', full_name='ont.rpc.keystore.RemoveRequest.names', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\210\265\030\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='allow_missing', full_name='ont.rpc.keystore.RemoveRequest.allow_missing', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=321,
  serialized_end=380,
)


_REMOVERESPONSE = _descriptor.Descriptor(
  name='RemoveResponse',
  full_name='ont.rpc.keystore.RemoveResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=382,
  serialized_end=398,
)


_GETONEREQUEST = _descriptor.Descriptor(
  name='GetOneRequest',
  full_name='ont.rpc.keystore.GetOneRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ont.rpc.keystore.GetOneRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\210\265\030\001'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=400,
  serialized_end=435,
)


_GETONERESPONSE = _descriptor.Descriptor(
  name='GetOneResponse',
  full_name='ont.rpc.keystore.GetOneResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='ont.rpc.keystore.GetOneResponse.value', index=0,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=437,
  serialized_end=490,
)


_GETREQUEST = _descriptor.Descriptor(
  name='GetRequest',
  full_name='ont.rpc.keystore.GetRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='names', full_name='ont.rpc.keystore.GetRequest.names', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='allow_missing', full_name='ont.rpc.keystore.GetRequest.allow_missing', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=492,
  serialized_end=542,
)


_GETRESPONSE_VALUESENTRY = _descriptor.Descriptor(
  name='ValuesEntry',
  full_name='ont.rpc.keystore.GetResponse.ValuesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ont.rpc.keystore.GetResponse.ValuesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ont.rpc.keystore.GetResponse.ValuesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=235,
  serialized_end=302,
)

_GETRESPONSE = _descriptor.Descriptor(
  name='GetResponse',
  full_name='ont.rpc.keystore.GetResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='ont.rpc.keystore.GetResponse.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_GETRESPONSE_VALUESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=545,
  serialized_end=686,
)


_WATCHREQUEST = _descriptor.Descriptor(
  name='WatchRequest',
  full_name='ont.rpc.keystore.WatchRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='names', full_name='ont.rpc.keystore.WatchRequest.names', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\210\265\030\001'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='allow_missing', full_name='ont.rpc.keystore.WatchRequest.allow_missing', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=688,
  serialized_end=746,
)


_WATCHRESPONSE_VALUESENTRY = _descriptor.Descriptor(
  name='ValuesEntry',
  full_name='ont.rpc.keystore.WatchResponse.ValuesEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ont.rpc.keystore.WatchResponse.ValuesEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='ont.rpc.keystore.WatchResponse.ValuesEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=235,
  serialized_end=302,
)

_WATCHRESPONSE = _descriptor.Descriptor(
  name='WatchResponse',
  full_name='ont.rpc.keystore.WatchResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='ont.rpc.keystore.WatchResponse.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='removed_values', full_name='ont.rpc.keystore.WatchResponse.removed_values', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_WATCHRESPONSE_VALUESENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=749,
  serialized_end=918,
)

_STOREREQUEST_VALUESENTRY.fields_by_name['value'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_STOREREQUEST_VALUESENTRY.containing_type = _STOREREQUEST
_STOREREQUEST.fields_by_name['values'].message_type = _STOREREQUEST_VALUESENTRY
_STOREREQUEST.fields_by_name['lifetime'].enum_type = _LIFETIME
_GETONERESPONSE.fields_by_name['value'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_GETRESPONSE_VALUESENTRY.fields_by_name['value'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_GETRESPONSE_VALUESENTRY.containing_type = _GETRESPONSE
_GETRESPONSE.fields_by_name['values'].message_type = _GETRESPONSE_VALUESENTRY
_WATCHRESPONSE_VALUESENTRY.fields_by_name['value'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_WATCHRESPONSE_VALUESENTRY.containing_type = _WATCHRESPONSE
_WATCHRESPONSE.fields_by_name['values'].message_type = _WATCHRESPONSE_VALUESENTRY
DESCRIPTOR.message_types_by_name['StoreRequest'] = _STOREREQUEST
DESCRIPTOR.message_types_by_name['StoreResponse'] = _STORERESPONSE
DESCRIPTOR.message_types_by_name['RemoveRequest'] = _REMOVEREQUEST
DESCRIPTOR.message_types_by_name['RemoveResponse'] = _REMOVERESPONSE
DESCRIPTOR.message_types_by_name['GetOneRequest'] = _GETONEREQUEST
DESCRIPTOR.message_types_by_name['GetOneResponse'] = _GETONERESPONSE
DESCRIPTOR.message_types_by_name['GetRequest'] = _GETREQUEST
DESCRIPTOR.message_types_by_name['GetResponse'] = _GETRESPONSE
DESCRIPTOR.message_types_by_name['WatchRequest'] = _WATCHREQUEST
DESCRIPTOR.message_types_by_name['WatchResponse'] = _WATCHRESPONSE
DESCRIPTOR.enum_types_by_name['Lifetime'] = _LIFETIME
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StoreRequest = _reflection.GeneratedProtocolMessageType('StoreRequest', (_message.Message,), {

  'ValuesEntry' : _reflection.GeneratedProtocolMessageType('ValuesEntry', (_message.Message,), {
    'DESCRIPTOR' : _STOREREQUEST_VALUESENTRY,
    '__module__' : 'minknow.rpc.keystore_pb2'
    # @@protoc_insertion_point(class_scope:ont.rpc.keystore.StoreRequest.ValuesEntry)
    })
  ,
  'DESCRIPTOR' : _STOREREQUEST,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.StoreRequest)
  })
_sym_db.RegisterMessage(StoreRequest)
_sym_db.RegisterMessage(StoreRequest.ValuesEntry)

StoreResponse = _reflection.GeneratedProtocolMessageType('StoreResponse', (_message.Message,), {
  'DESCRIPTOR' : _STORERESPONSE,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.StoreResponse)
  })
_sym_db.RegisterMessage(StoreResponse)

RemoveRequest = _reflection.GeneratedProtocolMessageType('RemoveRequest', (_message.Message,), {
  'DESCRIPTOR' : _REMOVEREQUEST,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.RemoveRequest)
  })
_sym_db.RegisterMessage(RemoveRequest)

RemoveResponse = _reflection.GeneratedProtocolMessageType('RemoveResponse', (_message.Message,), {
  'DESCRIPTOR' : _REMOVERESPONSE,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.RemoveResponse)
  })
_sym_db.RegisterMessage(RemoveResponse)

GetOneRequest = _reflection.GeneratedProtocolMessageType('GetOneRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETONEREQUEST,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.GetOneRequest)
  })
_sym_db.RegisterMessage(GetOneRequest)

GetOneResponse = _reflection.GeneratedProtocolMessageType('GetOneResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETONERESPONSE,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.GetOneResponse)
  })
_sym_db.RegisterMessage(GetOneResponse)

GetRequest = _reflection.GeneratedProtocolMessageType('GetRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETREQUEST,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.GetRequest)
  })
_sym_db.RegisterMessage(GetRequest)

GetResponse = _reflection.GeneratedProtocolMessageType('GetResponse', (_message.Message,), {

  'ValuesEntry' : _reflection.GeneratedProtocolMessageType('ValuesEntry', (_message.Message,), {
    'DESCRIPTOR' : _GETRESPONSE_VALUESENTRY,
    '__module__' : 'minknow.rpc.keystore_pb2'
    # @@protoc_insertion_point(class_scope:ont.rpc.keystore.GetResponse.ValuesEntry)
    })
  ,
  'DESCRIPTOR' : _GETRESPONSE,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.GetResponse)
  })
_sym_db.RegisterMessage(GetResponse)
_sym_db.RegisterMessage(GetResponse.ValuesEntry)

WatchRequest = _reflection.GeneratedProtocolMessageType('WatchRequest', (_message.Message,), {
  'DESCRIPTOR' : _WATCHREQUEST,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.WatchRequest)
  })
_sym_db.RegisterMessage(WatchRequest)

WatchResponse = _reflection.GeneratedProtocolMessageType('WatchResponse', (_message.Message,), {

  'ValuesEntry' : _reflection.GeneratedProtocolMessageType('ValuesEntry', (_message.Message,), {
    'DESCRIPTOR' : _WATCHRESPONSE_VALUESENTRY,
    '__module__' : 'minknow.rpc.keystore_pb2'
    # @@protoc_insertion_point(class_scope:ont.rpc.keystore.WatchResponse.ValuesEntry)
    })
  ,
  'DESCRIPTOR' : _WATCHRESPONSE,
  '__module__' : 'minknow.rpc.keystore_pb2'
  # @@protoc_insertion_point(class_scope:ont.rpc.keystore.WatchResponse)
  })
_sym_db.RegisterMessage(WatchResponse)
_sym_db.RegisterMessage(WatchResponse.ValuesEntry)


_STOREREQUEST_VALUESENTRY._options = None
_STOREREQUEST.fields_by_name['values']._options = None
_REMOVEREQUEST.fields_by_name['names']._options = None
_GETONEREQUEST.fields_by_name['name']._options = None
_GETRESPONSE_VALUESENTRY._options = None
_WATCHREQUEST.fields_by_name['names']._options = None
_WATCHRESPONSE_VALUESENTRY._options = None

_KEYSTORESERVICE = _descriptor.ServiceDescriptor(
  name='KeyStoreService',
  full_name='ont.rpc.keystore.KeyStoreService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1012,
  serialized_end=1412,
  methods=[
  _descriptor.MethodDescriptor(
    name='store',
    full_name='ont.rpc.keystore.KeyStoreService.store',
    index=0,
    containing_service=None,
    input_type=_STOREREQUEST,
    output_type=_STORERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='remove',
    full_name='ont.rpc.keystore.KeyStoreService.remove',
    index=1,
    containing_service=None,
    input_type=_REMOVEREQUEST,
    output_type=_REMOVERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='get_one',
    full_name='ont.rpc.keystore.KeyStoreService.get_one',
    index=2,
    containing_service=None,
    input_type=_GETONEREQUEST,
    output_type=_GETONERESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='get',
    full_name='ont.rpc.keystore.KeyStoreService.get',
    index=3,
    containing_service=None,
    input_type=_GETREQUEST,
    output_type=_GETRESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='watch',
    full_name='ont.rpc.keystore.KeyStoreService.watch',
    index=4,
    containing_service=None,
    input_type=_WATCHREQUEST,
    output_type=_WATCHRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_KEYSTORESERVICE)

DESCRIPTOR.services_by_name['KeyStoreService'] = _KEYSTORESERVICE

# @@protoc_insertion_point(module_scope)
