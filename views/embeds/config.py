import discord
import utils.helpers.snake_to_normal as s2n

def create_config_embed(configData):
    embed = discord.Embed(
        title="Servoskull Parameters",
        description="Current parameters set by the archmagos.",
        color=discord.Color.darker_grey()
    )
        
    embed.add_field(name="Guild ID", value=str(configData.get("guild_id", "N/A")), inline=True)
    embed.add_field(name="Default Event Announcement Channel", value=f"<#{configData.get('default_event_channel', 'N/A')}>", inline=True)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="Default Event Name", value=configData.get("default_event_name", "N/A"), inline=True)
    embed.add_field(name="Default Event Location", value=configData.get("default_event_location", "N/A"), inline=True)
    embed.add_field(name="", value="", inline=False)
    embed.add_field(name="Enable Automatic Polling", 
                    value=":x:" if configData.get("enable_automatic_polling", 0) == 0 else
                    ":white_check_mark:" if configData.get("enable_automatic_polling", 0) == 1 else
                    str(configData.get("enable_automatic_polling", "N/A")), inline=True)
    embed.add_field(name="Default Polling Time", value=str(configData.get("default_polling_time", "N/A")), inline=True)
    embed.add_field(name="Note", value="To change these parameters, use the `/config` commands.", inline=False)
    
    return embed
    