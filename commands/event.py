from datetime import datetime
import discord
from discord.ext import pages
from models.event import *
from models.config import get_config_for_guild
from views.pagination.event_list import create_event_list
from views.embeds.event import event_embed

def setup(bot):
    # Create the event command group
    event = bot.create_group(
        "event", "These commands help you manage events."
    )
    
    def format_event_choices(events):
        from discord import OptionChoice

        return [
            OptionChoice(
                name=f"{event['id']} - {event['name']} - {event['date']}",
                value=str(event['id'])
            )
            for event in events
        ]

    
    @event.command()
    async def new(
        ctx,
        name = discord.Option(
            str,
            description="The name of the event",
            required=True,
            max_length=50,
        ),
        date = discord.Option(
            str,
            description="The date of the event (e.g., DD-MM-YYYY HH:M)",
            required=True,
            min_length=16,
            max_length=16,
        ),
        location = discord.Option(
            str,
            description="The location of the event",
            default="To be determined",
            max_length=50,
        ),
        channel = discord.Option(
            discord.TextChannel,
            description="The channel where the event will be announced",
            default=None,
        ),
    ):
        """Create a new event."""
        try:
            # Fetch the guild configuration
            config = get_config_for_guild(ctx.guild.id)
            
            valid_datetime = datetime.strptime(date, "%d-%m-%Y %H:%M")
            
            create_event(
                guild_id=ctx.guild.id,
                user_id=ctx.author.id,
                channel_id=channel.id if channel else config["default_event_channel"],
                event_name=name,
                event_date=valid_datetime,
                event_location=location
            )
            
            latest_event = get_latest_event(ctx.guild.id, channel.id)
            if latest_event is None:
                latest_event['id'] = 'not found'
                await ctx.respond("Error retrieving the newly created event. Check list to see if it was created.")
            
            embed = await event_embed(latest_event, bot, context="new")
            await ctx.respond(embed=embed)
        except ValueError:
            # Handle invalid time format
            await ctx.respond(
                f"Invalid time format: **{date}**. Please use the format DD-MM-YYYY HH:MM."
            )

    @event.command()
    async def edit(
        ctx,
        event_id = discord.Option(
            str,
            description="The name of the event",
            max_length=50,
            required=False,
        ),
        name = discord.Option(
            str,
            description="The name of the event",
            max_length=50,
            required=False,
        ),
        date = discord.Option(
            str,
            description="The date of the event (e.g., DD-MM-YYYY HH:M)",
            required=False,
            min_length=16,
            max_length=16,
        ),
        location = discord.Option(
            str,
            description="The location of the event",
            max_length=50,
            required=False,
        ),
        channel = discord.Option(
            discord.TextChannel,
            description="The channel where the event will be announced",
            required=False,
        ),
        reason = discord.Option(
            str,
            description="Reason for editing the event",
            max_length=140,
            min_length=10,
            required=True
        ),
    ):
        try:
            if date is not None:
                valid_datetime = datetime.strptime(date, "%d-%m-%Y %H:%M")

            # Fetch the target event details
            target_event = get_event_by_id(event_id)

            # Compare and use the values from target_event if identical or None
            name = name if name and name != target_event['name'] else target_event['name']
            valid_datetime = valid_datetime if date and valid_datetime != target_event['date'] else target_event['date']
            location = location if location and location != target_event['location'] else target_event['location']
            channel = channel if channel and channel.id != target_event['channel_id'] else target_event['channel_id']
            
            """Edit an existing event."""
            edit_event(
                event_id,
                channel=channel.id if channel else None,
                event_name=name,
                event_date=valid_datetime if date else None,
                event_location=location if location else "To be determined",
                user_id=ctx.author.id,
                reason=reason if reason else "No reason provided",
            )

            edited_event = get_event_by_id(event_id)
            embed = await event_embed(edited_event, bot, context="edit")
            await ctx.respond(embed=embed)
        except ValueError:
            # Handle invalid time format
            await ctx.respond(
                f"Invalid time format: **{date}**. Please use the format DD-MM-YYYY HH:MM."
            )

    @event.command()
    async def cancel(ctx, event_id: str):
        """Cancel an event."""
        cancel_event(int(event_id.split(" - ")[0]), ctx.author.id)
        await ctx.respond(f"Event ID {event_id.split(' - ')[0]} has been cancelled.")

    @event.command()
    async def uncancel(ctx, event_id: int):
        """Uncancel an event."""
        uncancel_event(event_id, ctx.author.id)
        await ctx.respond(f"Event ID {event_id} has been uncancelled.")

    @event.command()
    async def list(ctx):
        """List all events for the current server."""
        events = get_events_for_guild(ctx.guild.id)
        if not events:
            await ctx.respond("No events found for this server.")
            return

        # Use the helper function to create embeds
        pages_list = create_event_list(events, title="Server Events")
        paginator = pages.Paginator(pages=pages_list)
        await paginator.respond(ctx.interaction)

    @event.command()
    async def my(ctx):
        """List all events for the user in the current server."""
        events = get_events_for_user_per_server(ctx.author.id, ctx.guild.id)
        if not events:
            await ctx.respond("You have no events in this server.")
            return
        
        # Use the helper function to create embeds
        pages_list = create_event_list(events, title="Your Events")
        paginator = pages.Paginator(pages=pages_list)
        await paginator.respond(ctx.interaction)