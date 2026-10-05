#!/usr/bin/env python3
"""Compatibility Codex entrypoint for the shared Harness runtime."""
from harness_runtime import config_for, contained, main, read_object, render_context, run_verification
import sys
if __name__ == '__main__': sys.exit(main())
