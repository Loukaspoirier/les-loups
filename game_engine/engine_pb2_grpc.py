# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import engine_pb2 as engine__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in engine_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class GameEngineStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterPlayer = channel.unary_unary(
                '/grpc.GameEngine/RegisterPlayer',
                request_serializer=engine__pb2.RegisterPlayerRequest.SerializeToString,
                response_deserializer=engine__pb2.RegisterPlayerResponse.FromString,
                _registered_method=True)
        self.MovePlayer = channel.unary_unary(
                '/grpc.GameEngine/MovePlayer',
                request_serializer=engine__pb2.MovePlayerRequest.SerializeToString,
                response_deserializer=engine__pb2.MovePlayerResponse.FromString,
                _registered_method=True)


class GameEngineServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterPlayer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def MovePlayer(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GameEngineServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterPlayer': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterPlayer,
                    request_deserializer=engine__pb2.RegisterPlayerRequest.FromString,
                    response_serializer=engine__pb2.RegisterPlayerResponse.SerializeToString,
            ),
            'MovePlayer': grpc.unary_unary_rpc_method_handler(
                    servicer.MovePlayer,
                    request_deserializer=engine__pb2.MovePlayerRequest.FromString,
                    response_serializer=engine__pb2.MovePlayerResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'grpc.GameEngine', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('grpc.GameEngine', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class GameEngine(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterPlayer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/grpc.GameEngine/RegisterPlayer',
            engine__pb2.RegisterPlayerRequest.SerializeToString,
            engine__pb2.RegisterPlayerResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def MovePlayer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/grpc.GameEngine/MovePlayer',
            engine__pb2.MovePlayerRequest.SerializeToString,
            engine__pb2.MovePlayerResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
