"""Sentry error reporting for openalex-sources (oxjob #1685): errors only, no PII.

Every scheduled job runs as `python -m jobs.<name>` (Advanced Scheduler), so
jobs/__init__.py calls init_sentry(); migrate.py (the release phase) calls it too.
An uncaught exception in a job is reported before the dyno exits. A no-op when
SENTRY_DSN is unset (local runs, tests).
"""
import os

import sentry_sdk

_initialized = False


def init_sentry():
    global _initialized
    dsn = os.environ.get("SENTRY_DSN")
    if _initialized or not dsn:
        return
    sentry_sdk.init(
        dsn=dsn,
        environment=os.environ.get("SENTRY_ENVIRONMENT", "production"),
        # HEROKU_* come from Heroku's runtime-dyno-metadata lab feature.
        release=os.environ.get("HEROKU_SLUG_COMMIT") or os.environ.get("HEROKU_RELEASE_VERSION"),
        server_name=os.environ.get("DYNO"),
        send_default_pii=False,
        traces_sample_rate=0,
    )
    _initialized = True
