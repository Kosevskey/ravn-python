"""Ravn — Error monitoring and performance tracking SDK for Python."""

import atexit
import functools
import os
import platform
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional

import requests

__version__ = "0.1.0"
__all__ = ["init", "capture_exception", "capture_message", "measure"]

_DEFAULT_API_URL = "https://app.getravn.com/api/v1/ingest"

_CONFIG: dict = {
    "api_key": None,
    "api_url": _DEFAULT_API_URL,
    "enabled": False,
    "slow_threshold_ms": 1000,
}

_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="ravn-worker")
atexit.register(lambda: _executor.shutdown(wait=True))


def _send_payload(payload: dict) -> None:
    headers = {
        "Content-Type": "application/json",
        "x-api-key": _CONFIG["api_key"],
    }
    try:
        requests.post(_CONFIG["api_url"], json=payload, headers=headers, timeout=3)
    except Exception:
        pass


def _base_metadata(extra: Optional[dict] = None) -> dict:
    meta: dict = {
        "sdk_version": __version__,
        "python_version": platform.python_version(),
        "platform": platform.system(),
        "cwd": os.getcwd(),
    }
    if extra:
        meta.update(extra)
    return meta


def capture_exception(exc: Exception, metadata: Optional[dict] = None) -> None:
    """Capture and report an exception to Ravn."""
    if not _CONFIG["enabled"]:
        return
    try:
        tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        payload = {
            "message": f"{type(exc).__name__}: {exc}",
            "level": "error",
            "metadata": _base_metadata({"stack_trace": tb, **(metadata or {})}),
        }
        _executor.submit(_send_payload, payload)
    except Exception:
        pass


def capture_message(
    message: str, level: str = "info", metadata: Optional[dict] = None
) -> None:
    """Send an arbitrary log message to Ravn."""
    if not _CONFIG["enabled"]:
        return
    try:
        payload = {
            "message": message,
            "level": level,
            "metadata": _base_metadata(metadata),
        }
        _executor.submit(_send_payload, payload)
    except Exception:
        pass


def _global_exception_handler(exc_type, exc_value, exc_traceback) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    capture_exception(exc_value, metadata={"mechanism": "unhandled_exception"})
    sys.__excepthook__(exc_type, exc_value, exc_traceback)


def init(
    api_key: str,
    api_url: Optional[str] = None,
    slow_threshold_ms: int = 1000,
) -> None:
    """Initialize the Ravn SDK.

    Args:
        api_key: Your Ravn project API key.
        api_url: Override the ingest endpoint (default: Ravn cloud).
        slow_threshold_ms: Performance alert threshold in milliseconds (default: 1000).
    """
    _CONFIG["api_key"] = api_key
    _CONFIG["enabled"] = True
    _CONFIG["slow_threshold_ms"] = slow_threshold_ms
    if api_url:
        _CONFIG["api_url"] = api_url
    sys.excepthook = _global_exception_handler
    print(f"[Ravn] Initialized (key: {api_key[:8]}…)")


def measure(func: Callable) -> Callable:
    """Decorator that reports slow function calls to Ravn.

    Usage:
        @ravn.measure
        def my_function():
            ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not _CONFIG["enabled"]:
            return func(*args, **kwargs)
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            duration_ms = (time.perf_counter() - start) * 1000
            if duration_ms > _CONFIG["slow_threshold_ms"]:
                capture_message(
                    f"Slow function: '{func.__name__}' took {duration_ms:.0f}ms",
                    level="warning",
                    metadata={
                        "function": func.__name__,
                        "module": func.__module__,
                        "duration_ms": round(duration_ms, 2),
                        "threshold_ms": _CONFIG["slow_threshold_ms"],
                    },
                )

    return wrapper