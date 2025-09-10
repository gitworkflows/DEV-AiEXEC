"""Settings constants for lfx package."""

import os

# Development mode flag - can be overridden by environment variable
DEV = os.getenv("AIEXEC_DEV", "false").lower() == "true"
