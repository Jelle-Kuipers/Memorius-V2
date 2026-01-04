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
    
    async def get_event_choices(ctx):
        """
        Fetch events for the current guild and return them as a list of strings for autocomplete.
        """
        events = get_events_for_guild(ctx.interaction.guild_id)
        return [
            discord.OptionChoice(
                name=f"{event['id']} - {event['event_name']} - {event['event_date']}",
                value=str(event['id'])
            )
            for event in events
        ]

    @event.command()
    async def new(
        ctx,
        name = discord.Option(
            str,
            name="event_name",
            description="The name of the event",
            required=True,
            max_length=50,
        ),
        date = discord.Option(
            str,
            name="event_date",
            description="The date of the event (e.g., DD-MM-YYYY HH:M)",
            required=True,
            min_length=16,
            max_length=16,
        ),
        location = discord.Option(
            str,
            name="event_location",
            description="The location of the event",
            required=False,
            max_length=50,
        ),
        channel = discord.Option(
            discord.TextChannel,
            name="announcement_channel",
            description="The channel where the event will be announced",
            required=False,
        ),
    ):
        """Create a new event."""
        try:
            # Fetch the guild configuration
            config = get_config_for_guild(ctx.guild.id)
            
            # Format the date before saving or displaying
            valid_datetime = datetime.strptime(date, "%d-%m-%Y %H:%M")
            formatted_date = valid_datetime.strftime("%d-%m-%Y %H:%M")

            create_event(
                guild_id=ctx.guild.id,
                user_id=ctx.author.id,
                channel_id=channel.id if channel else config["default_event_channel"],
                event_name=name,
                event_date=formatted_date,  # Save the formatted date
                event_location=location if location else config["default_event_location"],
            )
            
            latest_event = get_latest_event(ctx.guild.id)
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
            name="event",
            description="Select an event to edit",
            autocomplete=get_event_choices,
            required=True,
        ),
        reason = discord.Option(
            str,
            name="edit_reason",
            description="Reason for editing the event",
            max_length=140,
            min_length=10,
            required=True
        ),
        name = discord.Option(
            str,
            name="event_name",
            description="The name of the event",
            max_length=50,
            required=False,
        ),
        date = discord.Option(
            str,
            name="event_date",
            description="The date of the event (e.g., DD-MM-YYYY HH:MM)",
            required=False,
            min_length=16,
            max_length=16,
        ),
        location = discord.Option(
            str,
            name="event_location",
            description="The location of the event",
            max_length=50,
            required=False,
        ),
        channel = discord.Option(
            discord.TextChannel,
            name="announcement_channel",
            description="The channel where the event will be announced",
            required=False,
        ),
    ):
        """Edit an existing event."""
        try:
            if date is not None:
                valid_datetime = datetime.strptime(date, "%d-%m-%Y %H:%M")

            # Fetch the target event details
            target_event = get_event_by_id(event_id)

            # Compare and use the values from target_event if identical or None
            name = name if name and name != target_event['event_name'] else target_event['event_name']
            valid_datetime = valid_datetime if date and valid_datetime != target_event['event_date'] else target_event['event_date']
            location = location if location and location != target_event['event_location'] else target_event['event_location']
            channel = channel if channel and channel.id != target_event['channel_id'] else target_event['channel_id']
            edited_by_id = ctx.author.id
            
            """Edit an existing event."""
            edited_event = edit_event(
                event_id,
                channel_id=channel.id if isinstance(channel, discord.TextChannel) else channel,
                event_name=name,
                event_date=valid_datetime,
                event_location=location,
                edited_by=edited_by_id,
                edited_reason=reason if reason else "No reason provided",
            )

            embed = await event_embed(edited_event, bot, context="edited")
            await ctx.respond(embed=embed)
        except ValueError:
            # Handle invalid time format
            await ctx.respond(
                f"Invalid time format: **{date}**. Please use the format DD-MM-YYYY HH:MM."
            )

    @event.command()
    async def cancel(
        ctx,
        event_id = discord.Option(
            str,
            name="event",
            description="Select an event to cancel",
            autocomplete=get_event_choices,
            required=True,
        ),
        reason = discord.Option(
            str,
            name="cancel_reason",
            description="Reason for cancelling the event",
            max_length=140,
            min_length=10,
            required=True
        ),
    ):
        """Cancel an event."""
        cancelled_event=cancel_event(event_id, ctx.author.id, reason)
        
        embed = await event_embed(cancelled_event, bot, context="cancelled")
        await ctx.respond(embed=embed)

    @event.command()
    async def uncancel(
        ctx,
        event_id = discord.Option(
            str,
            name="event",
            description="Select an event to uncancel",
            autocomplete=get_event_choices,
            required=True,
        ),
        reason = discord.Option(
            str,
            name="cancel_reason",
            description="Reason for uncancelling the event",
            max_length=140,
            min_length=10,
            required=True
        ),
    ):
        """Cancel an event."""
        cancelled_event=uncancel_event(event_id, ctx.author.id, reason)
        
        embed = await event_embed(cancelled_event, bot, context="uncancelled")
        await ctx.respond(embed=embed)

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
        
    @event.command()
    async def view(
        ctx,
        event_id = discord.Option(
            str,
            name="event",
            description="Select an event to view",
            autocomplete=get_event_choices,
            required=True,
        ),
    ):
        """View details of a specific event."""
        event_data = get_event_by_id(event_id)
        if not event_data:
            await ctx.respond(f"Event with ID {event_id} not found.")
            return
        
        embed = await event_embed(event_data, bot, context="read")
        await ctx.respond(embed=embed)