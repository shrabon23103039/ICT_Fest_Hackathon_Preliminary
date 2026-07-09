"""Thread-safe human-facing booking reference codes."""
import threading
import time
_counter = {"value": 1000}
_lock = threading.Lock()

def _format_pause() -> None:
    time.sleep(0.12)

def next_reference_code() -> str:
    with _lock:
        current = _counter["value"]
        _format_pause()
        _counter["value"] = current + 1
        return f"CW-{current:06d}"
