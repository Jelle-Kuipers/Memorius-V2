import logging
import sys

from .tables.events import (
    init_db as init_events_db,
    add_event,
    edit_event,
    cancel_event,
    uncancel_event,
    get_events_for_guild,
    get_events_for_user_per_server,
    get_latest_event,
    get_event_by_id,
    clean_old_events,
)
from .tables.configs import (
    init_db as init_config_db,
    add_config,
    get_config,
    update_default_event_channel,
    update_default_event_name,
    update_default_event_location,
    update_enable_automatic_polling,
    update_default_polling_time,
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