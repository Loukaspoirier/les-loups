# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: engine.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'engine.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x65ngine.proto\x12\x04grpc\"9\n\x15RegisterPlayerRequest\x12\x0e\n\x06pseudo\x18\x01 \x01(\t\x12\x10\n\x08party_id\x18\x02 \x01(\x05\"<\n\x16RegisterPlayerResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x11\n\tplayer_id\x18\x02 \x01(\x05\"\x9a\x01\n\x11MovePlayerRequest\x12\x11\n\tplayer_id\x18\x01 \x01(\x05\x12\x1b\n\x13origin_position_col\x18\x02 \x01(\t\x12\x1b\n\x13origin_position_row\x18\x03 \x01(\t\x12\x1b\n\x13target_position_col\x18\x04 \x01(\t\x12\x1b\n\x13target_position_row\x18\x05 \x01(\t\"%\n\x12MovePlayerResponse\x12\x0f\n\x07message\x18\x01 \x01(\t2\x9a\x01\n\nGameEngine\x12K\n\x0eRegisterPlayer\x12\x1b.grpc.RegisterPlayerRequest\x1a\x1c.grpc.RegisterPlayerResponse\x12?\n\nMovePlayer\x12\x17.grpc.MovePlayerRequest\x1a\x18.grpc.MovePlayerResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'engine_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTERPLAYERREQUEST']._serialized_start=22
  _globals['_REGISTERPLAYERREQUEST']._serialized_end=79
  _globals['_REGISTERPLAYERRESPONSE']._serialized_start=81
  _globals['_REGISTERPLAYERRESPONSE']._serialized_end=141
  _globals['_MOVEPLAYERREQUEST']._serialized_start=144
  _globals['_MOVEPLAYERREQUEST']._serialized_end=298
  _globals['_MOVEPLAYERRESPONSE']._serialized_start=300
  _globals['_MOVEPLAYERRESPONSE']._serialized_end=337
  _globals['_GAMEENGINE']._serialized_start=340
  _globals['_GAMEENGINE']._serialized_end=494
# @@protoc_insertion_point(module_scope)
