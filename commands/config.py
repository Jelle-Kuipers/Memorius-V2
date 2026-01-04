import datetime
import discord
from models.config import *
from views.embeds.config import create_config_embed

# Server Specific Configurations

def setup(bot):
    # Create the event command group
    config = bot.create_group(
        "config", "These commands help you manage the bots config."
    )
    
    @config.command()
    async def get(ctx):
        """Get the current server configuration."""
        configData = get_config_for_guild(ctx.guild.id)
        embed = create_config_embed(configData)
        await ctx.respond(embed=embed)
        
    @config.command()
    async def default_event_channel(
        ctx, 
        channel = discord.Option(
            discord.SlashCommandOptionType.channel,
            channel_types=[discord.ChannelType.text],
        )
    ):    
        """Set the default event channel."""
        update_default_event_channel(ctx.guild.id, channel.id)
        await ctx.respond(f"Default event channel set to {channel.mention}.")
    
    @config.command()
    async def default_polling_time(
        ctx,
        time = discord.Option(
            str,
            description="Time in HH:MM format (24-hour clock)",
            default="02:00",
            max_length=5,
            min_length=5
        )
    ):
        """Set the default polling time for default events."""
        try:
            # Validate the time format (e.g., HH:MM)
            valid_time = datetime.datetime.strptime(time, "%H:%M").time()
            update_default_polling_time(ctx.guild.id, valid_time)
            await ctx.respond(f"Default polling time set to **{time}**.")
        except ValueError:
            # Handle invalid time format
            await ctx.respond(
                f"Invalid time format: **{time}**. Please use the format HH:MM (e.g., 02:00)."
            )
    
    @config.command()
    async def default_event_location(
        ctx, 
        location = discord.Option(
            str, 
            "Default location for events", 
            default="To be determined",
            max_length=50
        )
    ):
        """Set the default location for events."""
        update_default_event_location(ctx.guild.id, location)
        await ctx.respond(f"Default location set to **{location}**.")
        
    @config.command()
    async def default_event_name(
        ctx, 
        name = discord.Option(
            str, 
            "Default name for events", 
            default="Event",
            max_length=50
        )
    ):
        """Set the default name for events."""
        update_default_event_name(ctx.guild.id, name)
        await ctx.respond(f"Default event name set to **{name}**.")
        
    @config.command()
    async def enable_automatic_polling(
        ctx,
        enable = discord.Option(
            bool,
            "Enable or disable automatic polling for default events",
            default=True
        )
    ):
        """Enable or disable automatic polling for default events."""
        update_enable_automatic_polling(ctx.guild.id, int(enable))
        status = "enabled" if enable else "disabled"
        await ctx.respond(f"Automatic polling has been **{status}**.")