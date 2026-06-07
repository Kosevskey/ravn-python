# ravn-sdk

The official Python SDK for [Ravn](https://getravn.com) — lightweight error monitoring and performance tracking for Python applications.

## Installation

```bash
pip install ravn-sdk
```

## Quick Start

```python
import ravn

ravn.init(api_key="your_api_key_here")
```

That's it. Ravn will now automatically capture all unhandled exceptions and report them to your dashboard.

## Features

### Automatic Exception Capture

After calling `ravn.init()`, any unhandled exception is automatically sent to Ravn — no try/except needed.

### Manual Exception Capture

```python
try:
    risky_operation()
except Exception as e:
    ravn.capture_exception(e, metadata={"user_id": 42})
```

### Log Messages

```python
ravn.capture_message("Payment processed", level="info", metadata={"amount": 99.99})
```

Supported levels: `info`, `warning`, `error`.

### Performance Monitoring

```python
@ravn.measure
def slow_database_query():
    ...
```

Functions decorated with `@ravn.measure` will automatically send a `warning` event to Ravn if they exceed `slow_threshold_ms` (default: 1000ms).

## Configuration

```python
ravn.init(
    api_key="your_api_key_here",
    api_url="https://app.getravn.com/api/v1/ingest",  # optional override
    slow_threshold_ms=500,  # warn if functions take longer than 500ms
)
```

## Requirements

- Python >= 3.8
- `requests >= 2.28`

## License

MIT
