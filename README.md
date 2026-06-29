# ravn-sdk

[![PyPI version](https://img.shields.io/pypi/v/ravn-sdk)](https://pypi.org/project/ravn-sdk/)
[![Python versions](https://img.shields.io/pypi/pyversions/ravn-sdk)](https://pypi.org/project/ravn-sdk/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**Error monitoring for Python — without the Sentry tax.**  
100,000 events/month free. AI-powered root cause analysis included. Setup in 30 seconds.

→ [getravn.com](https://getravn.com) · [Dashboard](https://app.getravn.com) · [Docs](https://docs.getravn.com)

---

## Install

```bash
pip install ravn-sdk
```

## Setup

```python
import ravn

ravn.init(api_key="your_api_key_here")
```

That's it. Every unhandled exception is now captured and sent to your Ravn dashboard — no try/except, no configuration overhead.

Get your API key at [app.getravn.com/register](https://app.getravn.com/register) — free, no credit card required.

---

## Features

### Automatic exception capture

After `ravn.init()`, all unhandled exceptions are captured automatically.

### Manual capture

```python
try:
    risky_operation()
except Exception as e:
    ravn.capture_exception(e, metadata={"user_id": 42})
```

### Log messages

```python
ravn.capture_message("Payment processed", level="info", metadata={"amount": 99.99})
```

Supported levels: `info`, `warning`, `error`.

### Performance monitoring

```python
@ravn.measure
def slow_database_query():
    ...
```

Functions decorated with `@ravn.measure` send a `warning` event if they exceed `slow_threshold_ms` (default: 1000ms).

---

## Configuration

```python
ravn.init(
    api_key="your_api_key_here",
    slow_threshold_ms=500,  # warn if functions take longer than 500ms
)
```

---

## Pricing

| Plan | Events/month | Price |
|---|---|---|
| Free | 100,000 | $0 — forever |
| Solo | 1,000,000 | $9.99/mo |
| Team | 10,000,000 | $19.99/mo |
| Business | 100,000,000 | $49.99/mo |

All paid plans include AI root cause analysis, Slack/Discord alerts, and performance monitoring.  
Full pricing at [getravn.com/pricing](https://getravn.com/pricing).

---

## Requirements

- Python ≥ 3.8
- `requests ≥ 2.28`

## License

MIT
