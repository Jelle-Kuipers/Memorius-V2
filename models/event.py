from utils.database.connection import get_connection
import logging

# Add new event
def create_event(guild_id, channel_id, user_id, event_name, event_date, event_location):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('INSERT INTO events (guild_id, channel_id, user_id, event_name, event_date, event_location) VALUES (?, ?, ?, ?, ?, ?)',
                      (guild_id, channel_id, user_id, event_name, event_date, event_location))
            conn.commit()
            logging.debug(f"Successfully added new event {event_name} for guild {guild_id}.")
    except Exception as e:
        logging.error(f"Database error: {e}")

# Edit existing event
def edit_event(event_id, channel_id, event_name, event_date, event_location, edited_by, edited_reason=None):
    try:
        with get_connection() as conn:
            c = conn.cursor()

            # Log the event_id and parameters for debugging
            logging.debug(f"Updating event ID {event_id} with parameters: channel_id={channel_id}, event_name={event_name}, event_date={event_date}, event_location={event_location}, edited_by={edited_by}, edited_reason={edited_reason}")

            # Execute the update query
            c.execute('UPDATE events SET channel_id = ?, event_name = ?, event_date = ?, event_location = ?, edited_at = CURRENT_TIMESTAMP, edited_by = ?, edited_reason = ? WHERE id = ?',
                      (channel_id, event_name, event_date, event_location, edited_by, edited_reason, event_id))

            # Log the number of rows affected
            logging.debug(f"Rows affected by update: {c.rowcount}")

            conn.commit()
            logging.debug(f"Successfully edited event ID {event_id}. Changes committed.")

            # Refetch the updated event to ensure the latest data is returned
            c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            row = c.fetchone()
            if row:
                columns = [desc[0] for desc in c.description]
                logging.debug(f"Refetched event data: {dict(zip(columns, row))}")
                return dict(zip(columns, row))
            logging.warning(f"Event ID {event_id} not found after update.")
            return None
    except Exception as e:
        logging.error(f"Database error: {e}")

# Cancel an event
def cancel_event(event_id, cancelled_by, reason):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE events SET cancelled = 1, cancelled_at = CURRENT_TIMESTAMP, cancelled_by = ?, edited_at = CURRENT_TIMESTAMP, edited_by = ?, edited_reason = ? WHERE id = ?',
                      (cancelled_by, cancelled_by, reason, event_id))
            conn.commit()
            logging.debug(f"Successfully cancelled event ID {event_id}.")
        # Refetch the cancelled event to ensure the latest data is returned
            c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            row = c.fetchone()
            if row:
                columns = [desc[0] for desc in c.description]
                logging.debug(f"Refetched event data: {dict(zip(columns, row))}")
                return dict(zip(columns, row))
            logging.warning(f"Event ID {event_id} not found after update.")
            return None
    except Exception as e:
        logging.error(f"Database error: {e}")

# Uncancel an event
def uncancel_event(event_id, edited_by, reason):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE events SET cancelled = 0, cancelled_at = NULL, cancelled_by = NULL, edited_at = CURRENT_TIMESTAMP, edited_by = ?, edited_reason = ? WHERE id = ?',
                      (edited_by, reason, event_id))
            conn.commit()
            logging.debug(f"Successfully uncancelled event ID {event_id}.")
        # Refetch the uncancelled event to ensure the latest data is returned
            c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            row = c.fetchone()
            if row:
                columns = [desc[0] for desc in c.description]
                logging.debug(f"Refetched event data: {dict(zip(columns, row))}")
                return dict(zip(columns, row))
            logging.warning(f"Event ID {event_id} not found after update.")
            return None
    except Exception as e:
        logging.error(f"Database error: {e}")

# Get all events for a guild
def get_events_for_guild(guild_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM events WHERE guild_id = ?', (guild_id,))
            columns = [desc[0] for desc in c.description]
            logging.debug(f"Successfully retrieved events for guild {guild_id}.")
            return [dict(zip(columns, row)) for row in c.fetchall()]
    except Exception as e:
        logging.error(f"Database error: {e}")

# Get all events for a specific user in a guild
def get_events_for_user_per_server(user_id, guild_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM events WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
            columns = [desc[0] for desc in c.description]
            logging.debug(f"Successfully retrieved events for user {user_id} in guild {guild_id}.")
            return [dict(zip(columns, row)) for row in c.fetchall()]
    except Exception as e:
        logging.error(f"Database error: {e}")
        
# Get the latest event in a guild.
def get_latest_event(guild_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM events WHERE guild_id = ? ORDER BY created_at DESC LIMIT 1', (guild_id,))
            row = c.fetchone()
            logging.debug(f"Successfully retrieved latest event for guild {guild_id}.")
            if row:
                columns = [desc[0] for desc in c.description]
                return dict(zip(columns, row))
            return None
    except Exception as e:
        logging.error(f"Database error: {e}")

# Get event by ID
def get_event_by_id(event_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            row = c.fetchone()
            logging.debug(f"Successfully retrieved event by ID {event_id}.")
            if row:
                columns = [desc[0] for desc in c.description]
                return dict(zip(columns, row))
            return None
    except Exception as e:
        logging.error(f"Database error: {e}")

# Clean old events (3 months old)
def clean_old_events():
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM events WHERE event_date < DATE("now", "-3 months")')
            conn.commit()
            logging.debug("Successfully cleaned old events older than 3 months.")
    except Exception as e:
        logging.error(f"Database error: {e}")

# Remove config
def delete_events_for_guild(guild_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM events WHERE guild_id = ?', (guild_id,))
            conn.commit()
            logging.debug(f"Successfully removed events for server {guild_id}.")
    except Exception as e:
        logging.error(f"Database error: {e}")