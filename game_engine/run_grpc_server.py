from concurrent import futures
import grpc
import time
from engine_pb2 import (
    RegisterPlayerResponse,
    MovePlayerResponse
)
from engine_pb2_grpc import (
    GameEngineServicer,
    add_GameEngineServicer_to_server
)
from engine import GameEngineService

class GameEngineServicer(GameEngineServicer):
    def __init__(self):
        self.engine = GameEngineService()

    def RegisterPlayer(self, request, context):
        try:
            player_id = self.engine.register_player(
                request.pseudo,
                request.party_id
            )
            return RegisterPlayerResponse(
                message="Inscription réussie",
                player_id=player_id
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return RegisterPlayerResponse()

    def MovePlayer(self, request, context):
        try:
            success = self.engine.move_player(
                player_id=request.player_id,
                origin_col=request.origin_position_col,
                origin_row=request.origin_position_row,
                target_col=request.target_position_col,
                target_row=request.target_position_row
            )
            return MovePlayerResponse(
                message="Déplacement effectué" if success else "Déplacement échoué"
            )
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return MovePlayerResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_GameEngineServicer_to_server(GameEngineServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Serveur gRPC démarré sur le port 50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()