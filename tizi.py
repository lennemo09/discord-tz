import os
from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TIMEZONES = {
    'Australia/Melbourne':'Melbourne',
    'Asia/Jakarta':'Vietnam',
    'Canada/Eastern':'Toronto/Canada Eastern',
    'Europe/Rome':'Italy/European Central'
}

TIMEZONES_CHOICES = [
                create_choice(
                    name="Melbourne",
                    value="Australia/Melbourne"
                ),
                create_choice(
                    name="Vietnam",
                    value="Asia/Jakarta"
                ),
                create_choice(
                    name="Toronto",
                    value="Canada/Eastern"
                ),
                create_choice(
                    name="Italy",
                    value="Europe/Rome"
                )
                ]

client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)

@slash.slash(
    name="tz",
    description="Convert the input timezone time to other preset timezones.",
    options=[
        create_option(
            name="source_timezone",
            description="What timezone is the given time?",
            required=True,
            option_type=3,
            choices=TIMEZONES_CHOICES),        
        create_option(
            name="time",
            description="The given time (HH:MM) to convert in 24-HR format (e.g. 19:30)",
            required=True,
            option_type=3
        ),
        create_option(
            name="destination_timezone",
            description="What timezone do you want to convert to? (Optional)",
            required=False,
            option_type=3,
            choices=TIMEZONES_CHOICES),
    ]
)

async def _tz(context:SlashContext, source_timezone:str, time:str, destination_timezone='all'):
    
    if destination_timezone != 'all':        
        new_time = convert_timezone(source_timezone,destination_timezone,time)
        await context.send(f'{time} in {TIMEZONES[source_timezone]} time is: {new_time} in {TIMEZONES[destination_timezone]} time.')
    else:
        message_string = f'{time} in {TIMEZONES[source_timezone]} time is:'
        
        for timezone_option in TIMEZONES:
            if timezone_option == source_timezone:
                continue
            else:
                new_time = convert_timezone(source_timezone,timezone_option,time)
                message_string += f'\n• {new_time} in {TIMEZONES[timezone_option]} time.'
        await context.send(message_string)
    
def convert_timezone(src_tz,dst_tz,t):
    """
    Requires Python 3.9 and run
    $ python -m pip install tzdata
    In order for time conversion to work
    """
    src_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, int(t[:2]), int(t[3:]), tzinfo=ZoneInfo(src_tz))
    dst_time = src_time.astimezone(ZoneInfo(dst_tz))
    
    return dst_time.strftime('%H:%M')

client.run(TOKEN)

