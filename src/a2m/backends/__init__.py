"""Optional accelerated backends.

Each backend is optional and has a local default, so every task runs on a plain CPU machine
with no GPU and no network. When a backend is installed or configured, the runner uses it as
an *additional* independent check or as a faster path - never as the only way to score a task.
"""
