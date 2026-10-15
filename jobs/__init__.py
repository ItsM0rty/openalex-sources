from sentry_setup import init_sentry

init_sentry()   # every scheduled job is `python -m jobs.<name>`, which imports this first (oxjob #1685)
