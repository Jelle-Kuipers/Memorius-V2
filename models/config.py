from utils.database.connection import get_connection
import logging

# Add new config
def add_config(guild_id, channel_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('INSERT INTO server_configs (guild_id, default_event_channel) VALUES (?, ?)',
                      (guild_id, channel_id))
            conn.commit()
            logging.debug(f"Successfully added new server config for server {guild_id}.")

    except Exception as e:
        logging.error(f"Database error: {e}")

# Get config
def get_config_for_guild(guild_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM server_configs WHERE guild_id = ?', (guild_id,))
            columns = [desc[0] for desc in c.description]
            row = c.fetchone()  # Fetch only the first row
            if row:
                logging.debug(f"Successfully retrieved config for server {guild_id}.")
                return dict(zip(columns, row))  # Return a single dictionary
            else:
                logging.warning(f"No config found for server {guild_id}.")
                return {}
    except Exception as e:
        logging.error(f"Database error: {e}")

# Update default event channel
def update_default_event_channel(guild_id, channel_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE server_configs SET default_event_channel = ? WHERE guild_id = ?',
                      (channel_id, guild_id))
            conn.commit()
            logging.debug(f"Successfully updated default event channel for server {guild_id}. Updated to {channel_id}.")
    except Exception as e:
        logging.error(f"Database error: {e}")

# Update default event name
def update_default_event_name(guild_id, event_name):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE server_configs SET default_event_name = ? WHERE guild_id = ?',
                      (event_name, guild_id))
            conn.commit()
            logging.debug(f"Successfully updated default event name for server {guild_id}. Updated to {event_name}.")
    except Exception as e:
        logging.error(f"Database error: {e}")

# Update default event location
def update_default_event_location(guild_id, event_location):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE server_configs SET default_event_location = ? WHERE guild_id = ?',
                      (event_location, guild_id))
            conn.commit()
            logging.debug(f"Successfully updated default event location for server {guild_id}. Updated to {event_location}.")
    except Exception as e:
        logging.error(f"Database error: {e}")

# Update enable automatic polling
def update_enable_automatic_polling(guild_id, enable_polling):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE server_configs SET enable_automatic_polling = ? WHERE guild_id = ?',
                      (enable_polling, guild_id))
            conn.commit()
            logging.debug(f"Successfully updated automatic polling for server {guild_id}. Updated to {enable_polling}.")
    except Exception as e:
        logging.error(f"Database error: {e}")

# Update default polling time
def update_default_polling_time(guild_id, polling_time):
    try:
        
        # Convert to time, as SQLite3 doesnt support datetime.time
        polling_time_str = polling_time.strftime("%H:%M")
        
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('UPDATE server_configs SET default_polling_time = ? WHERE guild_id = ?',
                      (polling_time_str, guild_id))
            conn.commit()
            logging.debug(f"Successfully updated default polling time for server {guild_id}. Updated to {polling_time}.")
    except Exception as e:
        logging.error(f"Database error: {e}")

# Remove config
def remove_config(guild_id):
    try:
        with get_connection() as conn:
            c = conn.cursor()
            c.execute('DELETE FROM server_configs WHERE guild_id = ?', (guild_id,))
            conn.commit()
            logging.debug(f"Successfully removed server config for server {guild_id}.")
    except Exception as e:
        logging.error(f"Database error: {e}")