# bug_report.md

## Confirmed fixes

1. **app/auth.py — access-token expiry**
   - Bug: multiplied the configured 15 minutes by 60, producing a 900-minute token.
   - Fix: use `timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)`.

2. **app/auth.py — logout revocation lookup**
   - Bug: checked revoked JTIs against `sub` (user id).
   - Fix: check the access token's `jti`.

3. **app/routers/auth.py + app/auth.py — refresh replay**
   - Bug: refresh tokens were reusable.
   - Fix: atomically consume each refresh-token JTI once.

4. **app/routers/auth.py — duplicate username**
   - Bug: duplicate username returned the existing user with 201.
   - Fix: return 409 `USERNAME_TAKEN`.

5. **app/timeutils.py — UTC offset normalization**
   - Bug: timezone offset was stripped without conversion.
   - Fix: convert to UTC first, then store naive UTC.

6. **app/routers/bookings.py — past-start grace window**
   - Bug: allowed starts up to five minutes in the past.
   - Fix: require `start > now`.

7. **app/routers/bookings.py — invalid duration**
   - Bug: zero/negative durations were not correctly rejected.
   - Fix: require 1–8 whole hours and `end > start`.

8. **app/routers/bookings.py — overlap boundaries**
   - Bug: `<=` rejected valid back-to-back bookings.
   - Fix: use `existing.start < new.end AND new.start < existing.end`.

9. **app/routers/bookings.py — booking concurrency**
   - Bug: conflict/quota check and insert were separate raceable operations.
   - Fix: protect the complete check-and-create critical section.

10. **app/services/ratelimit.py — rate-limit race**
    - Bug: concurrent requests could lose bucket updates.
    - Fix: atomic bucket trim/append/check.

11. **app/services/reference.py + app/models.py — duplicate reference codes**
    - Bug: counter issuance raced under concurrency.
    - Fix: serialize issuance and add a database uniqueness constraint.

12. **app/routers/bookings.py — pagination**
    - Bug: descending order, wrong offset, and hard-coded limit 10.
    - Fix: ascending start/id, `(page-1)*limit`, requested limit.

13. **app/routers/bookings.py — booking visibility**
    - Bug: members could read another member's booking in the same org.
    - Fix: return 404 unless owner or same-org admin.

14. **app/routers/bookings.py — corrupted detail start_time**
    - Bug: response overwrote booking start time with created time.
    - Fix: preserve serializer output.

15. **app/routers/bookings.py + app/services/refunds.py — refund tiers/rounding**
    - Bug: exact 48h boundary wrong, under-24h returned 50%, and rounding was inconsistent.
    - Fix: correct 100/50/0 tiers and Decimal `ROUND_HALF_UP`; response uses stored ledger amount.

16. **app/routers/bookings.py + app/models.py — concurrent cancellation**
    - Bug: two cancels could create two refund rows.
    - Fix: atomic cancellation critical section and unique refund-per-booking constraint.

17. **app/services/export.py — cross-tenant export**
    - Bug: `include_all=true&room_id=...` could export another org's room.
    - Fix: every export query is scoped by organization.

18. **app/routers/bookings.py — stale usage report / availability**
    - Bug: create and cancel did not invalidate both affected caches.
    - Fix: invalidate report and availability on both lifecycle changes.

19. **app/services/notifications.py — deadlock**
    - Bug: create and cancel acquired email/audit locks in opposite order.
    - Fix: consistent lock order.

20. **app/routers/rooms.py — stats correctness**
    - Bug: process-memory incremental stats could drift under races and reset on restart.
    - Fix: calculate count/revenue directly from confirmed bookings in the database.
