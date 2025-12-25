"""
Centralized runtime configuration.

This file defines tunable parameters for the agent system.
Values can later be overridden by environment variables if needed.
"""

# ---- Agent execution limits ----
MAX_STEPS = 20
MAX_RETRIES = 2

# ---- LLM configuration ----
OPENAI_MODEL = "gpt-4o-mini"
TEMPERATURE = 0.2

# ---- Tool settings ----
DATA_DIR = "data"
WEB_SEARCH_TIMEOUT = 10