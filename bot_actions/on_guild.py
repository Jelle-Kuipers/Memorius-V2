from models.config import add_config, remove_config
from models.event import delete_events_for_guild
import logging

async def on_guild_join(guild):
    """Triggered when the bot joins a new server."""
    logging.debug(f"Joined a new server: {guild.name} (ID: {guild.id})")

    # Run the create_configuration command (assumed to be add_config)
    try:
            # Find the first text channel the bot can write in
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                default_channel = channel.id
                logging.debug(f"First writable channel in {guild.name}: {channel.name} (ID: {channel.id})")
                break
        
        add_config(guild.id, default_channel)
        logging.debug(f"Configuration created for server {guild.name} (ID: {guild.id}).")
    except Exception as e:
        logging.error(f"Failed to create configuration for server {guild.name} (ID: {guild.id}): {e}")

async def on_guild_remove(guild):
    """Triggered when the bot is removed from a server."""
    logging.debug(f"Removed from server: {guild.name} (ID: {guild.id})")
    # Additional cleanup can be done here if necessary
    
    try:
        logging.debug(f"Starting cleanup for server {guild.name} (ID: {guild.id}).")
        logging.debug(f"Start Cleanup for Events Table")
        delete_events_for_guild(guild.id)
        logging.debug(f"Cleanup completed for Events Table")
        logging.debug(f"Start Cleanup for Configs Table")
        remove_config(guild.id)
        logging.debug(f"Cleanup completed for Configs Table")
        logging.debug(f"Cleanup completed for server {guild.name} (ID: {guild.id}).")
    except Exception as e:
        logging.error(f"Failed to cleanup for server {guild.name} (ID: {guild.id}): {e}")