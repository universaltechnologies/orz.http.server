import threading
import urllib.request

import pytest

from orz.http.server import Handler


PORT = 18765


@pytest.fixture(scope="module")
def serve(tmp_path_factory):
    """Start one server for all tests in this module."""
    import http.server

    tmp = tmp_path_factory.mktemp("www")
    (tmp / "index.html").write_bytes(b"ok")
    (tmp / "test.js.br").write_bytes(b"br")
    (tmp / "test.wasm.gz").write_bytes(b"gz")
    (tmp / "test.js").write_bytes(b"js")
    (tmp / "a.js.br").write_bytes(b"br")
    (tmp / "a.wasm.gz").write_bytes(b"gz")
    (tmp / "a.mjs.br").write_bytes(b"br")

    class DirServer(http.server.HTTPServer):
        def finish_request(self, request, client_address):
            self.RequestHandlerClass(request, client_address, self, directory=str(tmp))

    httpd = DirServer(("localhost", PORT), Handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    yield PORT
    httpd.shutdown()


def get(port, path="/"):
    r = urllib.request.urlopen(f"http://localhost:{port}{path}")
    return dict(r.headers), r.read()


class TestHeaders:
    def test_coop(self, serve):
        headers, _ = get(serve)
        assert headers["Cross-Origin-Opener-Policy"] == "same-origin"

    def test_coep(self, serve):
        headers, _ = get(serve)
        assert headers["Cross-Origin-Embedder-Policy"] == "require-corp"

    def test_br_encoding(self, serve):
        headers, _ = get(serve, "/test.js.br")
        assert headers["Content-Encoding"] == "br"

    def test_gz_encoding(self, serve):
        headers, _ = get(serve, "/test.wasm.gz")
        assert headers["Content-Encoding"] == "gzip"

    def test_no_encoding_for_plain(self, serve):
        headers, _ = get(serve, "/test.js")
        assert "Content-Encoding" not in headers


class TestMime:
    def test_js_br(self, serve):
        headers, _ = get(serve, "/a.js.br")
        assert "javascript" in headers["Content-type"]

    def test_wasm_gz(self, serve):
        headers, _ = get(serve, "/a.wasm.gz")
        assert "wasm" in headers["Content-type"]

    def test_mjs_br(self, serve):
        headers, _ = get(serve, "/a.mjs.br")
        assert "javascript" in headers["Content-type"]
