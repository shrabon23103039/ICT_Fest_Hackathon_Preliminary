"""Simulated booking lifecycle side effects with consistent lock ordering."""
import threading
import time
_email_lock = threading.Lock()
_audit_lock = threading.Lock()

def _send_email(kind: str, booking) -> None:
    time.sleep(0.12)

def _write_audit(kind: str, booking) -> None:
    time.sleep(0.1)

def notify_created(booking) -> None:
    with _email_lock:
        _send_email("created", booking)
        with _audit_lock:
            _write_audit("created", booking)

def notify_cancelled(booking) -> None:
    with _email_lock:
        _send_email("cancelled", booking)
        with _audit_lock:
            _write_audit("cancelled", booking)
