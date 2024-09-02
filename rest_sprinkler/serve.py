import os
import http.server
import socketserver
from typing import Type
from textwrap import dedent
from http import HTTPStatus

from .ha import Client as HaClient

USER_AGENT = "rest_sprinkler"

client = HaClient(
    base_url="https://home-assistant.snow.jflei.com",
    api_token=os.environ["HA_API_TOKEN"],
    user_agent=USER_AGENT,
)


class Handler(http.server.SimpleHTTPRequestHandler):
    server_version = USER_AGENT

    def do_GET(self):
        try:
            self._router()
        except:
            self._five_oh_oh()
            raise

    def _router(self):
        parts = self.path.removeprefix("/").split("/")

        if len(parts) == 2:
            entity_id, verb = parts
            self._call_service(entity_id, verb)
        else:
            self._usage()

    def _five_oh_oh(self):
        self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        self.end_headers()

    def _usage(self):
        self.send_response(HTTPStatus.BAD_REQUEST)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        usage = dedent(
            """\
            Usage: GET /[entity_id]/[service]

            Examples:

                GET /switch.garage_outlet_storage_underside_lights/turn_on

                GET /switch.garage_outlet_storage_underside_lights/turn_off
            """
        )
        self.wfile.write(bytes(usage.encode()))

    def _call_service(self, entity_id: str, service: str):
        client.call_service(
            domain="switch",
            service=service,
            entity_id=entity_id,
        )
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()


class HttpServer(socketserver.TCPServer):
    allow_reuse_address = True

    def __init__(
        self,
        bind_address: str,
        port: int,
        Handler: Type[http.server.SimpleHTTPRequestHandler],
    ):
        super().__init__((bind_address, port), Handler)

    def serve_forever(self):
        ip, port = server.server_address
        print(f"Server started at http://{ip}:{port}")

        super().serve_forever()


if __name__ == "__main__":
    server = HttpServer("127.0.0.1", 8081, Handler)
    server.serve_forever()
