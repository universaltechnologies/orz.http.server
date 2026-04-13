import contextlib
import socket
import subprocess
import threading
import http.server
from mcp.server.fastmcp import FastMCP
from orz.http.server import Handler

mcp = FastMCP("orz.http.server")

_server = None
_thread = None


@mcp.tool()
def start_server(port: int = 8080, directory: str = ".") -> str:
    """Start a static HTTP server with Cross-Origin isolation headers for high-resolution timers."""
    global _server, _thread
    if _server:
        return f"already running on port {_server.server_address[1]}"
    Handler.directory = directory

    class DualStackServer(http.server.ThreadingHTTPServer):
        def server_bind(self):
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0
                )
            return super().server_bind()

    _server = DualStackServer(("localhost", port), Handler)
    _thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _thread.start()
    return f"serving on http://localhost:{port}"


@mcp.tool()
def stop_server() -> str:
    """Stop the HTTP server."""
    global _server, _thread
    if not _server:
        return "not running"
    _server.shutdown()
    _server = None
    _thread = None
    return "stopped"


@mcp.tool()
def server_status() -> str:
    """Check if the HTTP server is running and on which port."""
    if _server:
        return f"running on port {_server.server_address[1]}"
    return "not running"


@mcp.tool()
def adb_reverse(port: int) -> str:
    """Forward an Android device port to the local host via adb."""
    result = subprocess.run(
        ["adb", "reverse", f"tcp:{port}", f"tcp:{port}"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        return f"adb reverse tcp:{port} tcp:{port} ok"
    return f"adb reverse failed: {result.stderr.strip()}"


@mcp.tool()
def adb_open_browser(port: int) -> str:
    """Open a URL in the Android device's browser via adb."""
    url = f"http://localhost:{port}"
    result = subprocess.run(
        ["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        return f"opened {url} on device"
    return f"adb open browser failed: {result.stderr.strip()}"


def cli():
    mcp.run()
