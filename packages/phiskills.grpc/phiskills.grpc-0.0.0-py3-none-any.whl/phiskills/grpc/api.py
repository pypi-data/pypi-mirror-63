from concurrent import futures
import signal
import sys
import argparse

import grpc


class Api:

    def __init__(self, name, max_workers=10, port=50051):
        self.name = name
        parser = argparse.ArgumentParser(description=f'${name} gRPC API Server')
        parser.add_argument('--port', type=int, default=port, help='custom port')
        self.port = parser.parse_args().port
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))

    def start(self, grace=60):
        self.server.add_insecure_port(f'[::]:{self.port}')
        self.server.start()
        print(f'${self.name} server running on port {self.port}')
        self.handle_termination(grace)
        self.server.wait_for_termination()

    def handle_termination(self, grace):
        def signal_handler(_sig, _frame):
            print(f'Termination requested: max {grace}s left')
            self.server.stop(grace)
            print(f'${self.name} server terminated')
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        signal.pause()
