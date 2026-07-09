"""Refund bookkeeping with exact half-up cent rounding."""
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session
from ..models import Booking, RefundLog

def log_refund(db: Session, booking: Booking, percent: int) -> RefundLog:
    amount_cents = int(
        (Decimal(booking.price_cents) * Decimal(percent) / Decimal(100))
        .quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    )
    entry = RefundLog(booking_id=booking.id, amount_cents=amount_cents,
                      status="processed", processed_at=datetime.utcnow())
    db.add(entry)
    return entry
