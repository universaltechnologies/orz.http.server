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
