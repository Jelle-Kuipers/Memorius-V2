import discord
import utils.helpers.format_datetime as fdt
from datetime import datetime

async def event_embed(event_data, bot, context):

    # We check the context or a specific state. Then we build the content of the embed.
    if event_data.get("cancelled") == 1 or context == "cancelled":
        cancelled_by_user = event_data.get("cancelled_by")
        if cancelled_by_user:
            title_text = "Event Cancelled"
            description_text = "This event has been cancelled. ID: **{}**".format(event_data.get("id", "N/A"))
            cancelled_user = await bot.fetch_user(cancelled_by_user)
            footer_text = "cancelled by {} at {} because: {}".format(
                cancelled_user.name,
                fdt.format_datetime(event_data.get("cancelled_at", "N/A")),
                event_data.get("edited_reason", "N/A")
            )
            discord_color = discord.Color.red()
        else:
            title_text = "Event Cancelled"
            description_text = "This event has been cancelled. ID: **{}**".format(event_data.get("id", "N/A"))
            footer_text = "cancelled by unknown user! at {} because: {}".format(
                fdt.format_datetime(event_data.get("cancelled_at", "N/A")),
                event_data.get("edited_reason", "N/A")
            )
            discord_color = discord.Color.red()
    elif context == "edited":
        edited_by_user = event_data.get("edited_by")
        if edited_by_user:
            title_text = "Event Edited"
            description_text = "This event has been edited. ID: **{}**".format(event_data.get("id", "N/A"))
            edited_user = await bot.fetch_user(edited_by_user)
            footer_text = "last edited by {} at {} because: {}".format(
                edited_user.name,
                fdt.format_datetime(event_data.get("edited_at", "N/A")),
                event_data.get("edited_reason", "N/A")
            )
            discord_color = discord.Color.blue()
        else:
            title_text = "Event Edited"
            description_text = "This event has been edited. ID: **{}**".format(event_data.get("id", "N/A"))
            edited_user = await bot.fetch_user(edited_by_user)
            footer_text = "last edited by unknown user! at {} because: {}".format(
                fdt.format_datetime(event_data.get("edited_at", "N/A")),
                event_data.get("edited_reason", "N/A")
            )
            discord_color = discord.Color.blue()
    elif context == "new":
        title_text = "Event Added"
        description_text = "A new event has been created. ID: **{}**".format(event_data.get("id", "N/A"))
        footer_text = "created at: {}".format(fdt.format_datetime(event_data.get("created_at", "N/A")))
        discord_color = discord.Color.green()
    elif context == "uncancelled":
        edited_by_user = event_data.get("edited_by")
        if edited_by_user:
            title_text = "Event Uncancelled"
            description_text = "This event has been uncancelled. ID: **{}**".format(event_data.get("id", "N/A"))
            edited_user = await bot.fetch_user(edited_by_user)
            footer_text = "last edited by {} at {} because: {}".format(
                edited_user.name,
                fdt.format_datetime(event_data.get("edited_at", "N/A")),
                event_data.get("edited_reason", "N/A")
            )
            discord_color = discord.Color.green()
        else:
            title_text = "Event Uncancelled"
            description_text = "This event has been uncancelled. ID: **{}**".format(event_data.get("id", "N/A"))
            edited_user = await bot.fetch_user(edited_by_user)
            footer_text = "last edited by unknown user! at {} because: {}".format(
                fdt.format_datetime(event_data.get("edited_at", "N/A")),
                event_data.get("edited_reason", "N/A")
            )
            discord_color = discord.Color.green()
    elif context == "read":
        title_text = "Event Details"
        description_text = "Details for event ID: **{}**".format(event_data.get("id", "N/A"))
        
        # If edited after creation, show that in footer.
        if event_data.get("edited_at") and event_data.get("edited_at") > event_data.get("created_at"):
            edited_by_user = event_data.get("edited_by")
            if edited_by_user:
                edited_user = await bot.fetch_user(edited_by_user)
                footer_text = "last edited by {} at {} because: {}".format(
                    edited_user.name,
                    fdt.format_datetime(event_data.get("edited_at", "N/A")),
                    event_data.get("edited_reason", "N/A")
                )
            else:
                footer_text = "last edited by unknown user! at {} because: {}".format(
                    fdt.format_datetime(event_data.get("edited_at", "N/A")),
                    event_data.get("edited_reason", "N/A")
                )
        else:
            footer_text = "created at: {}".format(fdt.format_datetime(event_data.get("created_at", "N/A")))
        
        # Set color if event is cancelled or not.
        if event_data.get("cancelled") == 1:
            discord_color = discord.Color.red()
        else:
            discord_color = discord.Color.dark_grey()
    else:
        title_text = "Event Information"
        description_text = "If you can read this, my creator fucked up!: **{}**".format(event_data.get("id", "N/A"))
        footer_text = "created at: {}".format(fdt.format_datetime(event_data.get("created_at", "N/A")))
        discord_color = discord.Color.purple()
        
    embed = discord.Embed(
        title=title_text,
        description=description_text,
        color=discord_color
    )
    
    # Set author to event creator
    event_creator = await bot.fetch_user(236862257705779200)
    embed.set_author(name=event_creator.name, icon_url=event_creator.display_avatar.url)

    # Never changes via conditions, only data.
    embed.add_field(name="Event Name", value=event_data.get("event_name", "N/A"), inline=False)
    embed.add_field(name="Event Date", value=fdt.format_datetime(event_data.get("event_date", "N/A")), inline=True)
    embed.add_field(name="Event Location", value=event_data.get("event_location", "N/A"), inline=True)
    embed.add_field(name="Announcement Channel", value=f"<#{event_data.get('channel_id', 'N/A')}>", inline=False)
    embed.add_field(name="Cancelled", value=":x: Event is cancelled :x:" if event_data.get("cancelled") == 1 else ":white_check_mark: Event is not cancelled! :white_check_mark: ", inline=False)
    embed.set_footer(text=footer_text)
    
    return embed