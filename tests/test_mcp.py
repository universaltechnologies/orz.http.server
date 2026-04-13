import subprocess
import urllib.request
from unittest.mock import patch

import pytest

from orz.http.mcp import start_server, stop_server, server_status, adb_reverse, adb_open_browser


@pytest.fixture(autouse=True)
def cleanup():
    """Ensure server is stopped after each test."""
    yield
    stop_server()


def get(port):
    r = urllib.request.urlopen(f"http://localhost:{port}")
    return dict(r.headers)


class TestStartServer:
    def test_starts_and_returns_url(self):
        result = start_server(18766, ".")
        assert result == "serving on http://localhost:18766"
        headers = get(18766)
        assert headers["Cross-Origin-Opener-Policy"] == "same-origin"

    def test_rejects_double_start(self):
        start_server(18767, ".")
        result = start_server(18768, ".")
        assert result == "already running on port 18767"


class TestStopServer:
    def test_stops_running_server(self):
        start_server(18769, ".")
        result = stop_server()
        assert result == "stopped"

    def test_stop_when_not_running(self):
        result = stop_server()
        assert result == "not running"

    def test_port_closed_after_stop(self):
        start_server(18770, ".")
        stop_server()
        with pytest.raises(Exception):
            urllib.request.urlopen("http://localhost:18770", timeout=2)


class TestServerStatus:
    def test_running(self):
        start_server(18771, ".")
        assert server_status() == "running on port 18771"

    def test_not_running(self):
        assert server_status() == "not running"


class TestRestartCycle:
    def test_start_stop_start(self):
        r1 = start_server(18772, ".")
        assert "serving" in r1
        stop_server()
        r2 = start_server(18773, ".")
        assert "serving" in r2
        assert server_status() == "running on port 18773"


class TestAdb:
    @patch("subprocess.run")
    def test_adb_reverse_ok(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess([], returncode=0)
        result = adb_reverse(8080)
        assert result == "adb reverse tcp:8080 tcp:8080 ok"

    @patch("subprocess.run")
    def test_adb_reverse_fail(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess([], returncode=1, stderr="error")
        result = adb_reverse(8080)
        assert "failed" in result

    @patch("subprocess.run")
    def test_adb_open_browser_ok(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess([], returncode=0)
        result = adb_open_browser(8080)
        assert result == "opened http://localhost:8080 on device"

    @patch("subprocess.run")
    def test_adb_open_browser_fail(self, mock_run):
        mock_run.return_value = subprocess.CompletedProcess([], returncode=1, stderr="error")
        result = adb_open_browser(8080)
        assert "failed" in result
