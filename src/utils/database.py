import os
from datetime import datetime
from pytz import timezone
from tinydb import TinyDB, Query

db = TinyDB('db.json')
table = db.table('discord')

TIMEZONE = timezone(os.getenv('TIMEZONE', 'Europe/Amsterdam'))

def utc_to_timezone(timestamp: str, timezone: str = TIMEZONE) -> str:
    """ Converts a timestamp from UTC to the timezone. """
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(timezone).strftime('%d/%m/%Y %H:%M:%S')


def timestamp_to_unix(timestamp: str) -> int:
    """ Converts a timestamp to unix time. """
    return int(datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S').timestamp())


def add_member_to_db(discord_id: int, profile_data: dict) -> (int | list[int]):
    """ Adds a member to the database. If the member already exists, it will update their profile data."""
    del profile_data['description']
    del profile_data['externalAppDisplayName']
    del profile_data['hasVerifiedBadge']
    del profile_data['isBanned']

    if profile_data['displayName'] == profile_data['name']:
        del profile_data['displayName']

    created_at = profile_data['created']
    del profile_data['created']

    created_at = utc_to_timezone(created_at)
    created_at = timestamp_to_unix(created_at)
    profile_data['created_at'] = created_at

    verified_at = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    verified_at = timestamp_to_unix(verified_at)

    data = {'discord_id': discord_id,
            'roblox_profile': profile_data, 'verified_at': verified_at}

    if table.search(Query().discord_id == discord_id):
        return table.update(data, Query().discord_id == discord_id)

    return table.insert(data)


def get_member_from_db(discord_id: int) -> dict:
    """ Returns the member's data from the database. """
    result = table.search(Query().discord_id == discord_id)
    if not result:
        return {}
    return table.search(Query().discord_id == discord_id)[0]
