# orz.http.server [![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=flat&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/universaltechnologies/orz.http.server)

[![test](https://github.com/universaltechnologies/orz.http.server/actions/workflows/test.yml/badge.svg)](https://github.com/universaltechnologies/orz.http.server/actions/workflows/test.yml)

A minimal HTTP server that sends Cross-Origin isolation headers, enabling high-resolution timers (`performance.now()` at microsecond precision) in the browser. Useful for Unity Profiler and other tools that depend on accurate timing.

Tested on Linux / Windows / macOS with Python 3.8+. MCP tools require Python 3.10+.

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
python -m orz.http.server port
```

## Android

Forward the port via adb, then open in Chrome:

```bash
adb reverse tcp:port tcp:port
```

```bash
adb shell am start -a android.intent.action.VIEW -d "http://localhost:port"
```

## Note

Always access via `localhost:port`, not `ip:port`.

## MCP Server

For AI assistants (Claude Code, Cursor, etc.):

```bash
pip install -e ".[mcp]"
```

Claude Code config:
```json
{
  "mcpServers": {
    "orz.http.server": {
      "command": "python",
      "args": ["-m", "mcp", "run", "orz.http.mcp:mcp"]
    }
  }
}
```

Tools: `start_server`, `stop_server`, `server_status`, `adb_reverse`, `adb_open_browser`

## FAQ

**Can I achieve this without code using the built-in `http.server`?**

No. The built-in `http.server` has no option to add custom headers or MIME type mappings.

**Does the MIME type mapping introduce security risks?**

No. It only tells the browser the correct file type. Correct MIME types actually help browser security policies work properly.

**Does enabling high-resolution timers expose me to attacks?**

No. The precision only applies to your own pages. COOP/COEP headers are opt-in — you're trusting your own pages, not opening access to others.

**Does this server work as a file server?**

Yes, it inherits `http.server` and serves directory contents. By default it serves the current directory, so use `-d path` to avoid exposing unwanted files.
