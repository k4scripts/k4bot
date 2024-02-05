import os
from modules.logger import logger
from datetime import datetime
from pytz import timezone
from tinydb import TinyDB, Query

db = TinyDB('db.json')
discord_table = db.table('discord')

TIMEZONE = timezone(os.getenv('TIMEZONE', 'Europe/Amsterdam'))


def utc_to_timezone(timestamp: str, timezone: str = TIMEZONE) -> str:
    """ Converts a timestamp from UTC to the timezone. """
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(timezone).strftime('%d/%m/%Y %H:%M:%S')


def timestamp_to_unix(timestamp: str) -> int:
    """ Converts a timestamp to unix time. """
    return int(datetime.strptime(timestamp, '%d/%m/%Y %H:%M:%S').timestamp())


def check_roblox_in_db(roblox_id: int) -> bool:
    """ Returns True if the Roblox ID is in the database, False otherwise. """
    return bool(discord_table.search(Query().roblox_profile['id'] == roblox_id))


def add_member_to_db(discord_id: int, profile_data: dict) -> (int | list[int]):
    """ Adds a member to the database. If the member already exists, it will update their profile data."""
    keys_to_remove = ['description', 'externalAppDisplayName',
                      'hasVerifiedBadge', 'isBanned']
    for key in keys_to_remove:
        del profile_data[key]

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

    if discord_table.search(Query().discord_id == discord_id):
        return discord_table.update(data, Query().discord_id == discord_id)

    return discord_table.insert(data)


def get_member_from_db(discord_id: int) -> dict:
    """ Returns the member's data from the database. """
    result = discord_table.search(Query().discord_id == discord_id)
    if not result:
        return {}
    return discord_table.search(Query().discord_id == discord_id)[0]


def remove_member_from_db(discord_id: int) -> int:
    """ Removes a member from the database. """
    return discord_table.remove(Query().discord_id == discord_id)


def clear_db(discord_id:int = 0) -> None:
    """ Clears the database. """
    
    if discord_id:
        logger.critical(f'Requested to clear the database by #{discord_id}.')
        
    if not discord_table.all():
        return
    
    with open('db.json.old', 'w') as backup_file:
        with open('db.json', 'r') as db_file:
            backup_file.write(db_file.read())
    
    logger.critical('Database has been cleared.')
    
    discord_table.truncate()