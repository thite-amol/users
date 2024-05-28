"""Module."""

import os
from pathlib import Path

BasePath = Path(__file__).resolve().parent.parent

# alembic Migration file storage path
ALEMBIC_Versions_DIR = os.path.join(BasePath, "alembic", "versions")

# Log file path
LOG_DIR = os.path.join(BasePath, "log")

# Mount static directory
STATIC_DIR = os.path.join(BasePath, "static")
