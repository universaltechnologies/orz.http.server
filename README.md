# orz.http.server

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
