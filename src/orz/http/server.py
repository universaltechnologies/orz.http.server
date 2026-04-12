import argparse
import contextlib
import http.server
import os
import socket

MIME = {
    ".html": "text/html",
    ".js": "application/javascript",
    ".mjs": "application/javascript",
    ".wasm": "application/wasm",
    ".data": "application/octet-stream",
}


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        if self.path.endswith(".br"):
            self.send_header("Content-Encoding", "br")
        elif self.path.endswith(".gz"):
            self.send_header("Content-Encoding", "gzip")
        super().end_headers()

    def guess_type(self, path):
        for ext, mime in MIME.items():
            if path.endswith(ext + ".br") or path.endswith(ext + ".gz"):
                return mime
        return super().guess_type(path)

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", metavar="ADDRESS")
    parser.add_argument("-d", "--directory", default=os.getcwd())
    parser.add_argument("-p", "--protocol", default="HTTP/1.0")
    parser.add_argument("port", default=8080, type=int, nargs="?")
    args = parser.parse_args()

    class DualStackServer(http.server.ThreadingHTTPServer):
        def server_bind(self):
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0
                )
            return super().server_bind()

        def finish_request(self, request, client_address):
            self.RequestHandlerClass(
                request, client_address, self, directory=args.directory
            )

    http.server.test(
        HandlerClass=Handler,
        ServerClass=DualStackServer,
        port=args.port,
        bind=args.bind,
        protocol=args.protocol,
    )


if __name__ == "__main__":
    main()
