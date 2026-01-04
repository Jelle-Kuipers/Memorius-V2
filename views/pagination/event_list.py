import datetime
import discord
import utils.helpers.format_datetime as fdt
from discord.ext import pages

def create_event_list(events, title="List of events"):
    """Helper function to create paginated embeds for events."""
    pages_list = []
    for i in range(0, len(events), 5):
        chunk = events[i:i+5]
        description = "\n\n".join([
            f"""
            **Event ID:** `{e['id']}` **Event Name:** {e['event_name']}
            **Date:** {fdt.format_datetime(e['event_date'])}
            **Location:** {e['event_location'] or 'N/A'}
            **Announcement Channel:** <#{e['channel_id']}>
            **Cancelled:** {':x: Event is cancelled :x:' if e['cancelled'] else ':white_check_mark: Event is not cancelled! :white_check_mark: '}
            """.strip()
            for e in chunk
        ])
        embed = discord.Embed(
            title=f"{title} (Page {i//5+1}/{(len(events)-1)//5+1})",
            description=description,
            color=discord.Color.blue()
        )
        pages_list.append(pages.Page(embeds=[embed]))
    return pages_list