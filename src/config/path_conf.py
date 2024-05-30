"""Base file to create path."""

import os
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent

# .env file path
DOTENV = os.path.join(BASE_PATH, "src", ".env")

SRC_PATH = os.path.join(BASE_PATH, "src")

# Log file path
LOG_DIR = os.path.join(BASE_PATH, "log")

# Mount static directory
STATIC_DIR = os.path.join(BASE_PATH, "static")
