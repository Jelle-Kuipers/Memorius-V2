import logging
import sys

from .tables.events import (
    init_db as init_events_db,
)
from .tables.configs import (
    init_db as init_config_db,
)

# Centralized initialization for all tables
def init_db():
    try:
        logging.debug("Initializing database tables...")
        logging.debug("Initializing events table...")
        init_events_db()
        logging.debug("Initializing configs table...")
        init_config_db()
        logging.debug("Database tables initialized successfully.")
    except Exception as e:
        logging.critical(f"Database initialization error: {e}")
        sys.exit(1)