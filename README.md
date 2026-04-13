# orz.http.server

A minimal HTTP server that sends Cross-Origin isolation headers, enabling high-resolution timers (`performance.now()` at microsecond precision) in the browser. Useful for Unity Profiler and other tools that depend on accurate timing.

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
